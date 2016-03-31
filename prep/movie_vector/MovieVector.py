class MovieVectorError(Exception):
    def __init__(self, movie_id, msg):
        self.message = "MovieVector <{}> : ".format(movie_id) + msg


import numpy as np

MISSING_FEAT = np.nan


class MovieVectorGenerator(object):
    """
    An abstract movie vector generator. All generators should inherit this and
    implement own logic.

    Set self.version to relevant version id.

    VECTOR_DESC = description of the movie vector.

    VECTOR_FORMAT is a vector describing the format of the generated movieVector
    VECTOR_FORMAT[i] = 0 if feature i is binary, 1 if categorical,
     2 if continuous

    """

    def __init__(self):
        self.version = 0
        self.VECTOR_FORMAT = None
        self.VECTOR_DESC = "No description :( "

        self._vectorizer = []
        self.header = [x[0] for x in self._vectorizer]

    def get_vector(self, movie):
        """
        :param movie: Instance a Movie object.
        :return: A vector representation of the movie.
        """
        vec = []
        for key, method in self._vectorizer:
            res = method(movie)
            vec.append(np.nan if res is None else res)
        return vec

    def get_dict(self, movie):
        return dict(zip(self.header, self.get_vector(movie)))

    def __repr__(self):
        return "MovieVector{}".format(self.version)

    def __str__(self):
        return "MovieVector{}".format(self.version)
