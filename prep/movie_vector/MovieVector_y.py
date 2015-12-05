import prep.movie_vector.vector_utils_y_changed as utils_y
from MovieVector import MovieVectorGenerator
from prep.IMDB import IMDB


class MovieVectorGenerator_y(MovieVectorGenerator):
    def __init__(self, imdb_conn=None):
        self.version = 4
        self.imdb_conn = IMDB() if imdb_conn is None else imdb_conn

        star_groups = [(0, 3), (3, 6), (6, 10)]

        gaga = ['rating']
        gaga += \
            ["genre avg rating", "director avg rating",
                "director in genres avg rating"]
        for i in xrange(0, 3):
            gaga += [
                "star_%s avg rating" % i,
                "star_%s & director avg rating" % i,
                "star_%s in genres avg rating" % i
            ]
        for i, j in star_groups:
            gaga += [
                "stars_%s-%s avg rating" % (i, j),
                "stars_%s-%s & director avg rating" % (i, j),
                "stars_%s-%s in genres avg rating" % (i, j)
            ]
        self.header = gaga

    def get_vector(self, movie):
        """
        :param movie: Instance of an object derived from Movie
        :return: A vector representation of the movie. The first value is
                the classification
        """
        return [x[1] for x in utils_y.vec_for_movie(self.imdb_conn, movie)]
