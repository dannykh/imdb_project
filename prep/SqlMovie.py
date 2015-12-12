import imdb_sql_consts as imdb_consts
from Movie import Movie, MovieError
from imdb_sql_consts import movie_role, info_type

_movie_queries = {
    "get_movie_main": "SELECT * FROM movie WHERE id=%s;",
    "get_movie_all": "",
    "get_rating": "SELECT rating from movie_year_rating WHERE movie_id=%s;",
    "get_full_cast": "SELECT id,role_id FROM cast_info WHERE movie_id=%s;",
    "get_cast_by_role": "SELECT person_id FROM cast_info WHERE movie_id=%s "
                        "AND role_id=%s;",
    "get_info_old": "SELECT info FROM movie_info WHERE info_type_id = %s "
                    "AND movie_id = %s;",
    "get_info_idx": "SELECT info FROM movie_info_idx WHERE info_type_id = %s "
                    "AND movie_id = %s;",
    "get_stars": "SELECT person_id FROM stars_temp WHERE "
                 "movie_id=%s AND `index`<=10 ORDER BY `index` ASC;",
    "get_actors": "SELECT person_id FROM cast_info WHERE movie_id=%s "
                  "AND role_id IN (1,2);",
    "get_cast_by_roles": "SELECT person_id,role_id FROM cast_info "
                         "WHERE movie_id=%s AND role_id IN %s ;",
    "get_info": "SELECT info,info_type_id FROM movie_info_all WHERE movie_id "
                "= %s "
                "AND info_type_id IN %s;"

}


class SqlMovie(dict):
    def __init__(self, imdb_conn, sql_id, mode=0, **kwrags):
        super(dict, self).__init__()
        if kwrags is not None:
            for key in kwrags:
                self[key] = kwrags[key]
        self._conn = imdb_conn
        self.id = sql_id
        self['id'] = self.id
        self['id'], self['title'], self['year'], self['imdb_index'], \
            self['rating'], self['votes'] = self._fetch_scalar("get_movie_main", sql_id)
        if mode == 1:
            self.update_fields()

    def __getattr__(self, item):
        return self[item]

    def __getstate__(self):
        return self.__dict__

    def update_fields(self, fields=None):
        self.load_cast()
        self.load_info()
        self.get_stars()
        self._normalize()

    def get_stars(self):
        if not self.has_key('stars'):
            self['stars'] = self._fetch_vec("get_stars", self.id)
            """
            if not self.stars:
                raise MovieError(self.id, "Movie has no stars")
            """
        return self.stars

    def get_directors(self):
        self.directors = self._get_by_role('director') \
            if self.directors is None else self.directors
        return self.directors

    def get_producers(self):
        self.producers = self._get_by_role('producer') \
            if self.producers is None else self.producers
        return self['producer']

    def get_actors(self):
        self.actors = self._get_by_role('actor') if self.actors is None else \
            self.actors
        return self.actors

    def _get_by_role(self, role_name):
        res = []
        role_id = movie_role[role_name]
        if self.cast is None:
            res = self._fetch_vec("get_cast_by_roles", self.id, tuple(role_id))
        else:
            res = [mem[0] for mem in self.cast if mem[1] == role_id]
        if not res:
            raise MovieError(self.id, "Movie has no %s" % role_name)
        return res

    def load_cast(self, roles=('actor', 'actress', 'producer', 'director')):
        tmp_cast = self._fetch_vec("get_cast_by_roles", self.id,
            tuple(movie_role[role] for role in roles))

        def __create_dict_entry(key, *aliases):
            return {key: [p[0] for p in tmp_cast if
                p[1] in (movie_role[nm] for nm in aliases)]}

        self.update(__create_dict_entry("actors", 'actor', 'actress'))
        self.update(__create_dict_entry("directors", 'director'))
        self.update(__create_dict_entry("producers", 'producer'))

        return self

    def load_info(self,
            single_infos=(
                    'gross', 'budget', 'plot', 'weekend gross', 'studios'),
            multi_infos=('genres', 'keywords', 'taglines')):
        infos = single_infos + multi_infos
        tmp_info = self._fetch_vec("get_info", self.id,
            tuple(info_type[info] for info in infos))

        for info in single_infos:
            self.update(
                {info: p[0] for p in tmp_info if p[1] == info_type[info]})

        for info in multi_infos:
            self.update(
                {info: [p[0] for p in tmp_info if p[1] == info_type[info]]})

        return self

    def _normalize(self):
        # TODO budget
        import re
        monetary = ['gross', 'budget']
        for key in monetary:
            if self.has_key(key) and self[key] is not None and self[key]:
                m = re.findall(r"([1-9][0-9,]+(\.\d)?)", self[key])
                self[key] = float(''.join(m[0][0].split(',')))

    def get_gross(self):
        if self.gross is None:
            self.gross = self._fetch_scalar("get_info", info_type['gross'],
                self.id)
        return self.gross

    def get_budget(self):
        # TODO : Normalize budget format
        if self.budget is None:
            self.budget = self._fetch_scalar("get_info", info_type['budget'],
                self.id)
        return self.budget

    def get_genres(self):
        if self.genres is None:
            self.genres = self._fetch_vec("get_info", info_type["genres"],
                self.id)
        return self.genres

    def __repr__(self):
        return "Movie : < Name = {} ({}). sql id = {}> ".format(self['title'],
            self['year'],
            self.id)

    def _fetch_vec(self, query_name, *args):
        return self._conn.fetch_vec(_movie_queries[query_name], *args)

    def _fetch_scalar(self, query_name, *args):
        return self._conn.fetch_scalar(_movie_queries[query_name], *args)
