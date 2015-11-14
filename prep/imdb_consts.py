from datetime import date

DB_DATE = date(2015, 5, 6)
ANFANG_DATE = date.min
NULL_RATING = (None, 0)


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class InputError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expr -- input expression in which the error occurred
        msg  -- explanation of the error
    """

    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg


class UnknownError(Error):
    """Exception raised for unknown errors.

    Attributes:
        in_expr -- some of the input expression of the function
        expr -- some of the problematic expressions
        msg  -- explanation of the error
    """

    def __init__(self, expr, in_expr, msg):
        self.expr = expr
        self.in_expr = in_expr
        self.msg = msg


class SizeError(Error):
    """Exception raised for unknown errors.

    Attributes:
        in_expr -- some of the input expression of the function
        expr -- some of the problematic expressions
        size -- vector the problematic expression's size
        msg  -- explanation of the error
    """

    def __init__(self, expr, in_expr, size, msg):
        self.expr = expr
        self.in_expr = in_expr
        self.size = size
        self.msg = msg


class PersonError(Error):
    def __init__(self, person_id):
        self.person_id = person_id


avg_queries = {
    "person avg rating": \
        "SELECT avg(info), COUNT(info) FROM movie_info_idx WHERE "
        "info_type_id = {} AND movie_id IN (" \
        "SELECT movie_id FROM cast_info WHERE role_id = {} AND person_id = {} )"
        " AND movie_id IN (" \
        "SELECT id FROM title WHERE {} <= production_year AND {} > production_year)",

    "persons avg rating": \
        "SELECT avg(info), COUNT(info) FROM movie_info_idx WHERE info_type_id = {}"
        " AND movie_id IN (" \
        "SELECT movie_id FROM cast_info WHERE role_id = {} AND person_id IN ({}) ) "
        "AND movie_id IN (" \
        "SELECT id FROM title WHERE {} <= production_year AND {} > production_year)",

    "person-director avg rating": \
        "SELECT AVG(info), COUNT(info) FROM movie_info_idx WHERE info_type_id = {}"
        " AND movie_id IN (" \
        "SELECT movie_id FROM cast_info WHERE role_id = {} AND person_id = {} "
        "AND movie_id IN (" \
        "SELECT movie_id FROM cast_info WHERE role_id = {} AND person_id = {})) "
        "AND movie_id IN (" \
        "SELECT id FROM title WHERE {} <= production_year AND {} > production_year);",

    "actor in genre avg rating": \
        "SELECT AVG(info), COUNT(info) FROM movie_info_idx WHERE info_type_id = {} "
        "AND movie_id IN (" \
        "SELECT movie_id FROM cast_info WHERE role_id = {} AND person_id = {} "
        "AND movie_id IN (" \
        "SELECT movie_id FROM movie_info WHERE info_type_id = {} AND info = '{}')) "
        "AND movie_id IN (" \
        "SELECT id FROM title WHERE {} <= production_year AND {} > production_year);",

    "actor in genres avg rating": \
        "SELECT AVG(info), COUNT(info) FROM movie_info_idx WHERE info_type_id = {} "
        "AND movie_id IN (" \
        "SELECT movie_id FROM cast_info WHERE role_id = {} AND person_id = {} "
        "AND movie_id IN (" \
        "SELECT movie_id FROM movie_info WHERE info_type_id = {} AND info IN ({}) ))"
        " AND movie_id IN (" \
        "SELECT id FROM title WHERE {} <= production_year AND {} > production_year);",

    "genre avg rating": \
        "SELECT AVG(info), COUNT(info) FROM movie_info_idx WHERE info_type_id = {} "
        "AND movie_id IN (" \
        "SELECT movie_id FROM movie_info WHERE info_type_id = {} AND info = '{}') "
        "AND movie_id IN (" \
        "SELECT id FROM title WHERE {} <= production_year AND {} > production_year);",

    "genres avg rating": \
        "SELECT AVG(info), COUNT(info) FROM movie_info_idx WHERE info_type_id = {} "
        "AND movie_id IN (" \
        "SELECT movie_id FROM movie_info WHERE info_type_id = {} AND info IN ({}) )"
        " AND movie_id IN (" \
        "SELECT id FROM title WHERE {} <= production_year AND {} > production_year);"
}

get_queries = {
    "movie stars": "SELECT person_id , `index` FROM stars_temp where movie_id = {} "
                   "order by `index`;",
    "movie participant": "SELECT person_id FROM cast_info where movie_id = {} "
                         "AND role_id = {};"
}

movie_role = {
    "actor": 1,
    "actress": 2,
    "producer": 3,
    "writer": 4,
    "cinematographer": 5,
    "composer": 6,
    "costume designer": 7,
    "director": 8,
    "editor": 9,
    "miscellaneous crew": 10,
    "production designer": 11,
    "guest": 12,

}

info_type = {
    "runtimes": 1,
    "genres": 3,
    "languages": 4,
    "taglines": 9,
    "keywords": 10,
    "soundtrack": 14,
    "quotes": 15,
    "release dates": 16,
    "locations": 18,
    "birth date": 21,
    "height": 22,
    "death date": 23,
    "plot": 98,
    "votes distribution": 99,
    "votes": 100,
    "rating": 101,
    "production dates": 102,
    "filming dates": 104,
    "budget": 105,
    "weekend gross": 106,
    "gross": 107,
    "opening weekend": 108,
    "studios": 111,
    "top 250 rank": 112,
    "bottom 10 rank": 113,

}

role_actor_gender = {
    "m": movie_role["actor"],
    "f": movie_role["actress"]
}


def year_to_date(year):
    return date(year, 1, 1)


def combine_avg(ratings):
    ratings_sum = ratings_num = 0
    for rating in ratings:
        if rating[1] > 0:
            ratings_sum += rating[0] * rating[1]
            ratings_num += rating[1]
    if ratings_num == 0:
        return None
    return ratings_sum / ratings_num
