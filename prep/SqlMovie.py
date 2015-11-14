import imdb_sql_consts as imdb_consts
from Movie import Movie, MovieError

_movie_queries = {
    "get_movie_main": "SELECT title,production_year FROM title WHERE id=%s;",
    "get_movie_all": "",
    "get_rating": "SELECT rating from movie_year_rating WHERE movie_id=%s;",
    "get_full_cast": "SELECT id,role_id FROM cast_info WHERE movie_id=%s;",
    "get_cast_by_role": "SELECT person_id FROM cast_info WHERE movie_id=%s "
                        "AND role_id=%s;",
    "get_info": "SELECT info FROM movie_info WHERE info_type_id = %s "
                "AND movie_id = %s;",
    "get_info_idx": "SELECT info FROM movie_info_idx WHERE info_type_id = %s "
                    "AND movie_id = %s;",
    "get_stars": "SELECT person_id FROM stars_temp WHERE "
                 "movie_id=%s AND `index`<=5 ORDER BY `index` ASC;",
}


class SqlMovie(Movie):
    def __init__(self, imdb_conn, sql_id, title=None, year=None, mode=0):
        super(SqlMovie, self).__init__()
        if id is None and title is None:
            raise MovieError(self.id, "Need either id or name")
        self.conn = imdb_conn
        self.id = sql_id
        self.title, self.year = title, year
        if title is None or year is None:
            self.title, self.year = self._fetch_scalar("get_movie_main",
                                                       self.id)
        if mode == 1:
            self.update()

    def update(self, fields=None):
        # TODO : allow field selection
        self.get_budget()
        self.get_directors()
        self.get_genres()
        self.get_stars()
        self.get_imdb_rating()
        self.get_producers()
        self.get_gross()

    def get_imdb_rating(self):
        if self.imdb_rating is None:
            self.imdb_rating = self._fetch_scalar("get_info_idx",
                                                  imdb_consts.info_type[
                                                      'rating'], self.id)
        return self.imdb_rating

    def get_stars(self):
        if self.stars is None:
            self.stars = self._fetch_vec("get_stars", self.id)
            if not self.stars:
                raise MovieError(self.id, "Movie has no stars")
        return self.stars

    def get_directors(self):
        if self.directors is None:
            self.directors = self._fetch_vec("get_cast_by_role", self.id,
                                             imdb_consts.movie_role['director'])
            if not self.directors:
                raise MovieError(self.id, "Movie_has_no_directors")
        return self.directors

    def get_producers(self):
        if self.producers is None:
            self.producers = self._fetch_vec("get_cast_by_role", self.id,
                                             imdb_consts.movie_role['producer'])
            if not self.producers:
                raise MovieError(self.id, "Movie has no producers")
        return self.producers

    def get_gross(self):
        if self.gross is None:
            self.gross = self._fetch_scalar("get_info",
                                            imdb_consts.info_type['gross'],
                                            self.id)
        return self.gross

    def __repr__(self):
        return "Movie : < Name = {} ({}). sql id = {}> ".format(self.title,
                                                                self.year,
                                                                self.id)

    def get_budget(self):
        # TODO : Normalize budget format
        if self.budget is None:
            self.budget = self._fetch_scalar("get_info",
                                             imdb_consts.info_type['budget'],
                                             self.id)
        return self.budget

    def get_genres(self):
        if self.genres is None:
            self.genres = self._fetch_vec("get_info",
                                          imdb_consts.info_type["genres"],
                                          self.id)
        return self.genres

    def _fetch_vec(self, query_name, *args):
        return self.conn.fetch_vec(_movie_queries[query_name], *args)

    def _fetch_scalar(self, query_name, *args):
        return self.conn.fetch_scalar(_movie_queries[query_name], *args)
