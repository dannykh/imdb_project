from SQLconnection import SQLconnection
import settings as db
from Movie import Movie
import cPickle as pkl

_queries = {
    "get_all_movies": u"SELECT id FROM title ORDER BY production_year ASC LIMIT %s;",
    "get_all_persons": u"SELECT id FROM name LIMIT %s;",
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
        self._movie_db = None

    def search_person(self, name, index):
        if index is None or index == -1:
            query = _queries["search_person"].format(name)
        else:
            query = _queries["search_person_indexed"].format(name, index)
        return self.conn.fetch_scalar(query)

    def get_movie(self, id, title=None, year=None):
        return SqlMovie(self.conn, id)

    def search_movie(self, name, year=None, *kwargs):
        if year is None:
            query = _queries["search_movie"].format(name)
        else:
            query = _queries['search_movie_with_year'].format(name, year)
        return self.conn.fetch_scalar(query)

    def get_all_movie_ids(self, limit=None):
        limit = 99999 if limit is None else limit
        return self.fetch_vec(_queries["get_all_movies"], limit)

    def get_all_movies(self, pkl_path='../data/movies.pkl', limit=None):
        if self._movie_db is None:
            with open(pkl_path, 'rb') as fp:
                self._movie_db = pkl.load(fp)

        for i, movie_dict in enumerate(self._movie_db):
            if not limit is None:
                if i == limit:
                    break
            yield Movie(self, movie_dict['id'], movie_dict)

    def fetch_scalar(self, query, *args):
        return self.conn.fetch_scalar(query, *args)

    def fetch_vec(self, query, *args):
        return self.conn.fetch_vec(query, *args)

    def execute_query(self, query, *args):
        return self.conn.execute_query(query, *args)


if __name__ == "__main__":
    conn = IMDB()
    i=0
    for res in conn.get_all_movies():
        i+=1
        print res
    print i