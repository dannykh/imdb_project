class MovieVectorError(Exception):
    def __init__(self, movie_id, msg):
        self.message = "MovieVector <{}> : ".format(movie_id) + msg


import numpy as np

MISSING_FEAT = np.nan


class MovieVectorGenerator(object):
    """
    An abstract movie vector generator. All generators should inherit this and
    implement own logic.
    First value in vector MUST BE the classification, like rating..
    Learning module should handle how to deal with classification, so
    should usually just leave first value as imdb_rating

    DO NOT FORGET TO SET self.version !!!!!

    VECTOR_DESC = description of the movie vector.

    VECTOR_FORMAT is a vector describing the format of the generated movieVector
    VECTOR_FORMAT[i] = 0 if feature i is binary, 1 if categorical,
     2 if continuous
     remember the first value is the classification, It's format should be
     included in VECTOR_FORMAT[0]

    """

    def __init__(self, classifier=None):
        """
        :param classifier: A function : Movie -> class. i.e function which,
                given a movie, returns it's classification.
        """
        self.version = 0
        self.VECTOR_FORMAT = None
        self.VECTOR_DESC = "No description :( "
        if classifier is None:
            self.classifier = lambda movie: movie.get_imdb_rating()
        else:
            self.classifier = classifier

    def get_vector(self, movie):
        """
        :param movie: Instance of an object derived from Movie
        :return: A vector representation of the movie. The first value is
                the classification
        """
        raise NotImplementedError

    def __repr__(self):
        return "MovieVector{}".format(self.version)

    def __str__(self):
        return "MovieVector{}".format(self.version)
