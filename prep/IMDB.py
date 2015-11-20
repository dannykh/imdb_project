from SQLconnection import SQLconnection
from SqlMovie import SqlMovie
from Person import Person
import settings as db

_queries = {
    "get_all_movies": u"SELECT id,title,production_year FROM title "
                      u"ORDER BY production_year ASC;",
    "search_movie": u"SELECT id FROM title WHERE title=\"{}\";",
    "search_person_indexed": u"SELECT id FROM name where name=\"{}\" AND"
                             u" imdb_index='{}' ;",
    "search_person": u"SELECT id FROM name where name=\"{}\";",
    "search_movie_with_year": u"SELECT id FROM title WHERE title=\"{}\" " \
                              u"AND production_year={};"
}


class IMDB:
    '''
    A connection object to the imdb database
    '''

    def __init__(self, host=db.DB_HOST, uname=db.DB_USER,
            password=db.DB_PSW, dbname=db.DB_NAME):
        self.db = dbname
        self.conn = SQLconnection(host, uname, password, dbname)
        self.conn.connect()

    def get_person(self, id):
        return Person(self.conn, id)

    def search_person(self, name, index):
        if index is None or index == -1:
            query = _queries["search_person"].format(name)
        else:
            query = _queries["search_person_indexed"].format(name, index)
        return self.conn.fetch_scalar(query)

    def get_movie(self, id, title=None, year=None):
        return SqlMovie(self.conn, id, title=title, year=year)

    def search_movie(self, name, year=None, *kwargs):
        if year is None:
            query = _queries["search_movie"].format(name)
        else:
            query = _queries['search_movie_with_year'].format(name, year)
        return self.conn.fetch_scalar(query)

    def update(self, obj):
        pass

    def get_all_movies(self, limit=None, query=None):
        if query is None:
            query = _queries["get_all_movies"]
        movie_ids = self.conn.fetch_query(query)
        limit = 9999 if limit is None else limit
        for movie_id in movie_ids:
            limit -= 1
            if limit <= 0:
                break
            yield self.get_movie(int(movie_id[0]), movie_id[1], movie_id[2])

    def fetch_scalar(self, query, *args):
        return self.conn.fetch_scalar(query, *args)

    def fetch_vec(self, query, *args):
        return self.conn.fetch_vec(query, *args)

    def execute_query(self, query, *args):
        return self.conn.execute_query(query, *args)
