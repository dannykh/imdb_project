__author__ = 'Danny'

from prep.imdb_sql_consts import movie_role, info_type, company_type, link_type
import re


class MovieError(Exception):
    def __init__(self, movie_id, msg):
        self.movie_id = movie_id
        self.message = "Movie <{}> : ".format(movie_id) + msg


_movie_queries = {
    "get_movie_main": "SELECT * FROM movie WHERE id=%s;",
    "get_rating": "SELECT rating from movie_year_rating WHERE movie_id=%s;",
    "get_full_cast": "SELECT id,role_id FROM cast_info WHERE movie_id=%s;",
    "get_cast_by_role": "SELECT person_id FROM cast_info WHERE movie_id=%s "
                        "AND role_id=%s;",
    "get_info_old": "SELECT info FROM movie_info WHERE info_type_id = %s "
                    "AND movie_id = %s;",
    "get_info_idx": "SELECT info FROM movie_info_idx WHERE info_type_id = %s "
                    "AND movie_id = %s;",
    "get_stars": "SELECT person_id FROM stars WHERE movie_id=%s  "
                 "ORDER BY `index` ASC;",
    "get_actors": "SELECT person_id FROM cast_info WHERE movie_id=%s "
                  "AND role_id IN (1,2);",
    "get_cast_by_roles": "SELECT person_id,role_id FROM cast_info "
                         "WHERE movie_id=%s AND role_id IN %s ;",
    "get_info": "SELECT info,info_type_id FROM movie_info WHERE movie_id = %s "
                "AND info_type_id IN %s;",
    "get_cast_full": "SELECT person_id,role_id FROM cast_info WHERE "
                     "movie_id = %s ;",
    "get_keywords": "SELECT keyword FROM keyword,movie_keyword "
                    "WHERE movie_id = %s AND keyword_id=keyword.id;",
    "get_companies": "SELECT company_id,company_type_id FROM movie_companies "
                     "WHERE movie_id = %s ;",
    "get_links": "SELECT linked_movie_id, link_type_id FROM movie_link "
                 "WHERE movie_id= %s AND link_type_id IN (1,2,3); ",
    "get_mpaa": "SELECT info FROM movie_info WHERE movie_id = %s AND info_type_id=97;",
    "get_actors_ordered": "SELECT person_id FROM actors WHERE movie_id = %s "
                          "ORDER BY `index` ASC ;"

}


class Movie(dict):
    _keys = [
        'id',
        'title',
        'year',
        'rating',
        'votes',
        'genres',
        'budget',
        'imdb id',
        'imdb index',
        'gross',
        'weekend gross',
        'stars',
        'actors',
        'directors',
        'writers',
        'producers',
        'cinematographers',
        'follows',
        'followed by',
        'remake of',
        'production companies',
        'special effects companies',
        'distributors',
        'taglines',
        'mpaa',
        'keywords',
        'studios',
        'runtimes',
        'languages',
        'composers',
        'costume designers',
        'editors',
        'production designers'
    ]

    def __init__(self, imdb_conn, sql_id, load=None):
        self.conn = imdb_conn
        for key in self._keys:
            self[key] = None
        self['id'] = sql_id
        if not load is None:
            for key, val in load.iteritems():
                if key in self._keys:
                    self[key] = val
        else:
            self.populate()

    def __getattr__(self, item):
        if not self.has_key(item):
            raise KeyError

        return self[item]

    def populate(self):
        self._get_basic_data()
        self._get_cast()
        self._get_info()
        self._get_keywords()
        self._get_companies()
        self._get_links()
        self._get_actors()
        self._normalize()

    def _get_basic_data(self):
        self['id'], self['title'], self['year'], self['imdb index'], self['imdb id'], \
            self['rating'], self['votes'] = self.conn.fetch_scalar(
            _movie_queries['get_movie_main'], self['id'])

    def _get_cast(self):
        cast = self.conn.fetch_vec(_movie_queries['get_cast_full'], self['id'])

        def __get_by_roles(*args):
            ids = [movie_role[role] for role in args]
            return [person[0] for person in cast if person[1] in ids]

        self['directors'] = __get_by_roles('director')
        self['producers'] = __get_by_roles('producer')
        self['cinematographers'] = __get_by_roles('cinematographer')
        self['composers'] = __get_by_roles('composer')
        self['costume designers'] = __get_by_roles('costume designer')
        self['writers'] = __get_by_roles('writer')
        self['production designers'] = __get_by_roles('production designer')
        self['editors'] = __get_by_roles('editor')

        self['stars'] = self.conn.fetch_vec(_movie_queries['get_stars'], self['id'])

    def _get_info(self):
        info_ids = [(info, info_type[info]) for info in self._keys if
            info_type.has_key(info)]

        all_info = self.conn.fetch_vec(_movie_queries['get_info'], self['id'],
            tuple(x[1] for x in info_ids))

        for info, info_id in info_ids:
            if self[info] is None:
                self[info] = [rec[0] for rec in all_info if rec[1] == info_id]

    def _get_keywords(self):
        self['keywords'] = self.conn.fetch_vec(_movie_queries['get_keywords'], self['id'])

    def _get_companies(self):
        companies = self.conn.fetch_vec(_movie_queries['get_companies'], self['id'])

        for company, company_type_id in company_type.iteritems():
            if company in self._keys:
                self[company] = [comp[0] for comp in companies if
                    comp[1] == company_type_id]

    def _get_links(self):
        links = self.conn.fetch_vec(_movie_queries['get_links'], self['id'])

        for link, link_id in link_type.iteritems():
            self[link] = [ln[0] for ln in links if ln[1] == link_id]

    def _get_actors(self):
        self['actors'] = self.conn.fetch_vec(_movie_queries['get_actors_ordered'],
            self['id'])

    def _normalize(self):
        # TODO convert currencies better
        self['mpaa'] = [info.split(' ')[1] for info in self['mpaa']]

        def __unlist(key):
            if type(self[key]) is list:
                self[key] = self[key][0] if self[key] else None

        singles = ['gross', 'weekend gross', 'budget']
        for x in singles:
            __unlist(x)

        monetary = ['gross', 'weekend gross', 'budget']
        for key in monetary:
            if self.has_key(key) and self[key] is not None and self[key]:
                if self[key].find('$') == -1 and self[key].find("€") == -1:
                    self[key] = None
                else:
                    coef = 1.12 if self[key].find("€") != -1 else 1
                    m = re.findall(r"([1-9][0-9,]+(\.\d)?)", self[key])
                    self[key] = float(''.join(m[0][0].split(','))) * coef

    def __repr__(self):
        return self['title'] + " (" + str(self['year']) + "). id=" + str(self['id'])
