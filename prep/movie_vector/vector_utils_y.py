from prep.imdb_consts import *
from prep.queries import queries_2


def combine_avg(ratings):
    ratings_sum, ratings_num = 0, 0
    for rating in ratings:
        if rating[1] > 0:
            ratings_sum += rating[0] * rating[1]
            ratings_num += rating[1]
    if ratings_num == 0:
        return NULL_RATING
    return ratings_sum / ratings_num


def check_years(from_year, to_year):
    if int(from_year) - int(to_year) > 0:
        raise InputError([from_year, to_year],
            "from_year is later than to_year")

    if int(to_year) - int(DB_DATE) > 0:
        raise InputError(to_year, "to_year is later than the db date")


def analyze_avg_result(avg_rating_mat, in_expr):
    if len(avg_rating_mat) == 0:
        return NULL_RATING, 0

    size = [len(avg_rating_mat), len(avg_rating_mat[0])]

    if size[0] != 1 or size[1] != 2:
        raise SizeError([avg_rating_mat], in_expr, size,
            "The size of this exp isn't right")

    avg_rating, movies_num = avg_rating_mat[0][0], avg_rating_mat[0][1]

    if movies_num == 0:
        return NULL_RATING, 0

    if avg_rating > 10 or avg_rating < 0 or movies_num < 0:
        raise UnknownError([avg_rating, movies_num], in_expr,
            "The avg rating or movies num is invalid")

    return avg_rating, movies_num


def person_avg_rating(imdb, id, role, from_year=ANFANG_DATE, to_year=DB_DATE):
    # TODO: check if person is in imdb
    check_years(from_year, to_year)
    """
    avg_rating_mat = _fetch_query(imdb, "person avg rating",
        info_type["rating"], role, id, from_year.year, to_year.year)
    """

    avg_rating_mat = imdb.fetch_vec(queries_2.person['avg_rating'], id, tuple(role),
        from_year, to_year)

    in_expr = [id, role, from_year, to_year]

    return analyze_avg_result(avg_rating_mat, in_expr)


def persons_avg_rating(imdb, ids, roles, from_year=ANFANG_DATE, to_year=DB_DATE):
    # WHAT SHOULD THIS DO ?!
    check_years(from_year, to_year)

    """
    person_str = get_string(ids, False)

    avg_rating_mat = _fetch_query(imdb, "persons avg rating",
        info_type["rating"], role, person_str, from_year.year, to_year.year)
    """

    avg_rating_mat = imdb.fetch_vec(queries_2.person['multi_avg_rating'], tuple(ids),
        tuple(roles), from_year, to_year)

    in_expr = [ids, roles, from_year, to_year]

    return analyze_avg_result(avg_rating_mat, in_expr)


def actor_director_avg_rating(imdb, actor_id, director_id,
        from_year=ANFANG_DATE, to_year=DB_DATE):
    check_years(from_year, to_year)

    """
    avg_rating_mat = _fetch_query(
        imdb, "person-director avg rating",
        info_type["rating"], actor_gender, actor_id, movie_role["director"],
        director_id, from_year.year, to_year.year)
    """

    avg_rating_mat = imdb.fetch_vec(queries_2.combined['person-director_avg_rating'],
        actor_id, (1, 2), director_id, from_year, to_year)

    in_expr = [actor_id, director_id, from_year, to_year]

    return analyze_avg_result(avg_rating_mat, in_expr)


def genre_avg_rating(imdb, genre, from_year=ANFANG_DATE, to_year=DB_DATE):
    """
    Deprecated. Use genres_ instead !

    """
    check_years(from_year, to_year)

    avg_rating_mat = _fetch_query(
        imdb, "genre avg rating", info_type["rating"], info_type["genres"],
        genre, from_year.year, to_year.year)

    in_expr = [genre, from_year, to_year]

    return analyze_avg_result(avg_rating_mat, in_expr)


def get_string(item_list, is_str=True):
    iten_str = ""

    for item in item_list:
        if iten_str != "":
            iten_str += ", "
        if is_str:
            iten_str += "'" + item + "'"
        else:
            iten_str += str(item)

    return iten_str


def genres_avg_rating(imdb, genres, from_year=ANFANG_DATE, to_year=DB_DATE):
    check_years(from_year, to_year)

    """
    avg_rating_mat = _fetch_query(
        imdb, "genres avg rating", info_type["rating"], info_type["genres"],
        genres, from_year.year, to_year.year)

    """

    avg_rating_mat = imdb.fetch_vec(queries_2.genre["avg_rating"], tuple(genres),
        from_year, to_year)

    in_expr = [genres, from_year, to_year]

    return analyze_avg_result(avg_rating_mat, in_expr)


def person_genre_avg_rating(imdb, id, role, genre, from_year=ANFANG_DATE,
        to_year=DB_DATE):
    """
    Deprecated : use person_genres_... instead !
    """
    check_years(from_year, to_year)

    avg_rating_mat = _fetch_query(
        imdb, "actor in genre avg rating", info_type["rating"], role, id,
        info_type["genres"], genre, from_year.year, to_year.year)

    in_expr = [id, role, genre, from_year, to_year]

    return analyze_avg_result(avg_rating_mat, in_expr)


def person_genres_avg_rating(imdb, id, role, genres, from_year=ANFANG_DATE,
        to_year=DB_DATE):
    check_years(from_year, to_year)

    """
    avg_rating_mat = _fetch_query(
        imdb, "actor in genres avg rating", info_type["rating"], role, id,
        info_type["genres"], genres, from_year.year, to_year.year)
    """

    avg_rating_mat = imdb.fetch_vec(queries_2.person["in_genres_avg"], id, tuple(role),
        tuple(genres), from_year, to_year)
    in_expr = [id, role, genres, from_year, to_year]

    return analyze_avg_result(avg_rating_mat, in_expr)


def _fetch_query(imdb, query_name, *args):
    return imdb.conn.fetch_query(avg_queries[query_name], *args)


def _fetch_get_query(imdb, query_name, *args):
    return imdb.conn.fetch_query(get_queries[query_name], *args)


def exp_wrp(func, def_res, year, **kwargs):
    try:
        return func(to_year=year, **kwargs)
    except InputError as e:
        print "{} : {}".format(e.msg, e.expr)
    except SizeError as e:
        print "{} : {} - {}, {}".format(e.msg, e.expr, e.size, e.in_expr)
    except UnknownError as e:
        print "{} : {}, {}".format(e.msg, e.expr, e.in_expr)
    return def_res


def exp_wrp_sq(func, one_dim=True, year=DB_DATE, **kwargs):
    if one_dim:
        return exp_wrp(func, NULL_RATING, year, **kwargs)[0]
    else:
        return exp_wrp(func, NULL_RATING, year, **kwargs)


def basic_movie_vec(conn, genres, director, year):
    g_r = exp_wrp_sq(genres_avg_rating, True, year, imdb=conn, genres=genres)
    d_r = exp_wrp_sq(person_avg_rating, True, year,
        imdb=conn, id=director, role=[movie_role["director"]])
    dg_r = exp_wrp_sq(person_genres_avg_rating, True, year,
        imdb=conn, id=director, role=[movie_role["director"]], genres=genres)
    return [
        ('Genres avg rating', g_r),
        ('Director avg rating', d_r),
        ("Director in Genres avg rating", dg_r)
    ]


def stars_movie_vec(conn, stars, genres, director, year):
    num_of_stars = len(stars)
    a_rs, ad_rs, ag_rs = [NULL_RATING] * num_of_stars, \
        [NULL_RATING] * num_of_stars, [NULL_RATING] * num_of_stars

    for i, star in enumerate(stars):
        # actor = conn.get_person(star)
        a_r = exp_wrp_sq(person_avg_rating, False, year,
            imdb=conn, id=star, role=(1, 2))
        ad_r = exp_wrp_sq(actor_director_avg_rating, False, year,
            imdb=conn, actor_id=star, director_id=director)
        ag_r = exp_wrp_sq(person_genres_avg_rating, False, year,
            imdb=conn, id=star, role=(1, 2), genres=genres)

        a_rs[i], ad_rs[i], ag_rs[i] = a_r, ad_r, ag_r

    stars_vec = []
    for i in xrange(0, 3):  # for 1st-3rd stars: add feat for each one.
        stars_vec += [
            ("Star_%s avg rating" % i, a_rs[i][0]),
            ("Star_%s & Director avg rating" % i, ad_rs[i][0]),
            ("Star_%s In Genres avg rating" % i, ag_rs[i][0])
        ]

    star_groups = [[0, 3], [3, 6], [6, 10]]
    for i, j in star_groups:
        stars_vec += [
            ("Stars_%s-%s avg rating" % (i, j), combine_avg(a_rs[i:j])),
            ("Stars_%s-%s & Director avg rating" % (i, j), combine_avg(ad_rs[i:j])),
            ("Stars_%s-%s In Genres avg rating" % (i, j), combine_avg(ag_rs[i:j]))
        ]

    return stars_vec


def vec_for_movie(conn, movie):
    genres = tuple(movie['genres'])
    director = movie['directors'][0]  # TODO : consider multiple directors
    year = movie['year']
    stars = movie['stars']

    movie_vec = [('rating', movie['rating'])] + basic_movie_vec(conn, genres, director,
        year) + stars_movie_vec(conn, stars, genres, director, year)

    return movie_vec
