__author__ = 'Danny'


class MovieError(Exception):
    def __init__(self, movie_id,msg):
        self.movie_id=movie_id
        self.message = "Movie <{}> : ".format(movie_id) + msg


class Movie(object):
    def __init__(self):
        self.title = None
        self.year = None
        self.id = None
        self.stars = None
        self.directors = None
        self.writers = None
        self.producers = None
        self.gross = None
        self.imdb_rating = None
        self.genres = None
        self.budget=None

    def update(self, fields=None):
        raise NotImplementedError

    def get_imdb_rating(self):
        return self.imdb_rating

    def get_producers(self):
        return self.producers

    def get_directors(self):
        return self.directors

    def get_gross(self):
        return self.gross

    def get_stars(self):
        return self.stars

    def get_budget(self):
        return self.budget

    def __repr__(self):
        return self.name + " (" + self.year + "). id=" + self.id

    def get_genres(self):
        return self.genres
