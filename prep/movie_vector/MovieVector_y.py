import prep.movie_vector.vector_utils_y_changed as utils_y
from movievector import MovieVectorGenerator
from prep.IMDB import IMDB
from prep.vector_utils_4 import get_movie_features, get_stars_avg_prio
#from vector_utils_4 import get_movie_features

HEADER_1 = [
    'Rating',
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
    'Is Comedy',
    'Is Thriller',
    'Is Romance',
    'Is Action',
    'Is Crime',
    'Is Adventure',
    'Is Horror',
    'Is Sci-Fi',
    'Is Mystery',
    'Is Fantasy',
    'Is Family',
    'Is Biography',
    'Is War',
    'Is Animation',
    'Is History',
    'Is Music',
    'Is Sport',
    'Is Musical',
    'Is Documentary'
]

HEADER_2 = ['Star_1 Smart Avg', 'Star_1 - Director Smart Avg', 'Star_2 Smart Avg', 'Star_2 - Director Smart Avg', 'Star_3 Smart Avg', 'Star_3 - Director Smart Avg', 'Stars 1 & 2', 'Stars 1 & 3', 'Stars 2 & 3', 'director smart avg rating', 'writer smart avg rating', 'composer smart avg rating']

HEADER = ['Star_1 a Avg', 'Star_1 s Avg', 'Star_1 a y Avg', 'Star_1 s y Avg', 'Star_1 a- Director Avg', 'Star_1 s- Director Avg', 'Star_1 a- Director y Avg', 'Star_1 s- Director y Avg', 'Star_2 a Avg', 'Star_2 s Avg', 'Star_2 a y Avg', 'Star_2 s y Avg', 'Star_2 a- Director Avg', 'Star_2 s- Director Avg', 'Star_2 a- Director y Avg', 'Star_2 s- Director y Avg', 'Star_3 a Avg', 'Star_3 s Avg', 'Star_3 a y Avg', 'Star_3 s y Avg', 'Star_3 a- Director Avg', 'Star_3 s- Director Avg', 'Star_3 a- Director y Avg', 'Star_3 s- Director y Avg']

class MovieVectorGenerator_y(MovieVectorGenerator):
    def __init__(self, imdb_conn=None):
        self.version = 4
        self.imdb_conn = IMDB() if imdb_conn is None else imdb_conn

        self.header = HEADER_2

    def get_vector(self, movie):
        """
        :param movie: Instance of an object derived from Movie
        :return: A vector representation of the movie. The first value is
                the classification
        """
        return [x[1] for x in get_movie_features  (self.imdb_conn, movie['id'], movie=movie)]
