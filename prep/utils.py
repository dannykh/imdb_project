from imdb_sql_consts import *
from queries_1 import avg_queries, get_queries


def get_movie_stars(imdb, movie_id):
    stars = []

    stars_mat = _fetch_get_query(imdb, "movie stars", [movie_id])

    num_of_stars = len(stars_mat)

    if num_of_stars == 0:
        raise InputError([movie_id],
            "There is no movie with the following id in the DB")

    if num_of_stars < 0 or num_of_stars > 10:
        raise UnknownError([num_of_stars], [movie_id], "")

    for star, index in stars_mat:
        stars += [star]

    return stars


def get_movie_participant(imdb, movie_id, role_type):
    participant_mat = _fetch_get_query(imdb, "movie participant",
        [movie_id, role_type])
    return participant_mat


def check_years(from_year, to_year):
    if (from_year - to_year).days > 0:
        raise InputError([from_year, to_year],
            "from_year is later than to_year")

    if (to_year - DB_DATE).days > 0:
        raise InputError(to_year, "to_year is later than the db date")

    return


def check_avg_result(avg_rating_mat, in_expr):
    if len(avg_rating_mat) == 0:
        return None, 0

    size = [len(avg_rating_mat), len(avg_rating_mat[0])]

    if size[0] != 1 or size[1] != 2:
        raise SizeError([avg_rating_mat], in_expr, size,
            "The size of this exp isn't right")

    avg_rating, movies_num = avg_rating_mat[0][0], avg_rating_mat[0][1]

    if movies_num == 0:
        return None, 0

    if avg_rating > 10 or avg_rating < 0 or movies_num < 0:
        raise UnknownError([avg_rating, movies_num], in_expr,
            "The avg rating or movies num is invalid")

    return avg_rating, movies_num


def person_avg_rating(imdb, id, role, from_year=ANFANG_DATE, to_year=DB_DATE):
    # TODO: check if person is in imdb
    check_years(from_year, to_year)

    avg_rating_mat = _fetch_query(imdb, "person avg rating",
        [info_type["rating"], role, id,
         from_year.year, to_year.year])

    in_expr = [id, role, from_year, to_year]

    return check_avg_result(avg_rating_mat, in_expr)


def persons_avg_rating(imdb, ids, role, from_year=ANFANG_DATE, to_year=DB_DATE):
    # TODO: check if person is in imdb
    check_years(from_year, to_year)

    person_str = get_string(ids, False)

    avg_rating_mat = _fetch_query(imdb, "persons avg rating",
        [info_type["rating"], role, person_str,
         from_year.year, to_year.year])

    in_expr = [id, role, from_year, to_year]

    return check_avg_result(avg_rating_mat, in_expr)


def actor_director_avg_rating(imdb, actor_id, actor_gender, director_id,
        from_year=ANFANG_DATE, to_year=DB_DATE):
    check_years(from_year, to_year)

    avg_rating_mat = _fetch_query(imdb, "person-director avg rating",
        [info_type["rating"], actor_gender, actor_id, \
         movie_role["director"], director_id,
         from_year.year, to_year.year])

    in_expr = [actor_id, actor_gender, director_id, from_year, to_year]

    return check_avg_result(avg_rating_mat, in_expr)


def genre_avg_rating(imdb, genre, from_year=ANFANG_DATE, to_year=DB_DATE):
    check_years(from_year, to_year)

    avg_rating_mat = _fetch_query(imdb, "genre avg rating",
        [info_type["rating"], info_type["genres"],
         genre, \
         from_year.year, to_year.year])

    in_expr = [genre, from_year, to_year]

    return check_avg_result(avg_rating_mat, in_expr)


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

    genres_str = get_string(genres)

    avg_rating_mat = _fetch_query(imdb, "genres avg rating",
        [info_type["rating"], info_type["genres"],
         genres_str, \
         from_year.year, to_year.year])

    in_expr = [genres, from_year, to_year]

    return check_avg_result(avg_rating_mat, in_expr)


def person_genre_avg_rating(imdb, id, role, genre, from_year=ANFANG_DATE,
        to_year=DB_DATE):
    check_years(from_year, to_year)

    avg_rating_mat = _fetch_query(imdb, "actor in genre avg rating",
        [info_type["rating"], role, id,
         info_type["genres"], genre, \
         from_year.year, to_year.year])

    in_expr = [id, role, genre, from_year, to_year]

    return check_avg_result(avg_rating_mat, in_expr)


def person_genre_avg_rating(imdb, id, role, genres, from_year=ANFANG_DATE,
        to_year=DB_DATE):
    check_years(from_year, to_year)

    genres_str = get_string(genres)

    avg_rating_mat = _fetch_query(imdb, "actor in genres avg rating",
        [info_type["rating"], role, id,
         info_type["genres"], \
         genres_str, from_year.year, to_year.year])

    in_expr = [id, role, genres, from_year, to_year]

    return check_avg_result(avg_rating_mat, in_expr)


def _fetch_query(imdb, query_name, *args):
    return imdb.conn.fetch_query(avg_queries[query_name].format(*args[0]))


def _fetch_get_query(imdb, query_name, *args):
    return imdb.conn.fetch_query(get_queries[query_name].format(*args[0]))


def vec_for_movie(conn, movie_id, movie=None):
    movie_vec = []

    if movie is None:
        movie = conn.get_movie(movie_id)

    genres = movie.get_genres()

    g_r = NULL_RATING

    try:
        g_r = genres_avg_rating(conn, genres, to_year=year_to_date(movie.year))
    except InputError as e:
        print "{} : {}".format(e.msg, e.expr)
    except SizeError as e:
        print "{} : {} - {}, {}".format(e.msg, e.expr, e.size, e.in_expr)
    except UnknownError as e:
        print "{} : {}, {}".format(e.msg, e.expr, e.in_expr)

    movie_vec += [g_r[0]]
    director_id = movie.directors[0]

    d_r = NULL_RATING
    dg_r = NULL_RATING
    try:
        d_r = person_avg_rating(conn, director_id, role_type["director"],
            to_year=date(movie.year, 1, 1))
        dg_r = person_genre_avg_rating(conn, director_id, role_type["director"],
            genres, \
            to_year=year_to_date(movie.year))

    except InputError as e:
        print "{} : {}".format(e.msg, e.expr)
    except SizeError as e:
        print "{} : {} - {}, {}".format(e.msg, e.expr, e.size, e.in_expr)
    except UnknownError as e:
        print "{} : {}, {}".format(e.msg, e.expr, e.in_expr)

    movie_vec += [d_r[0], dg_r[0]]
    stars = _get_movie_stars_w(conn, movie_id)
    num_of_stars = len(stars)
    a_rs, ad_rs, ag_rs = [NULL_RATING] * num_of_stars, [
        NULL_RATING] * num_of_stars, [NULL_RATING] * num_of_stars

    for index, star in enumerate(stars):
        actor = conn.get_person(star)
        a_r, ad_r, ag_r = NULL_RATING, NULL_RATING, NULL_RATING
        try:
            a_r = person_avg_rating(conn, star, role_actor_gender[actor.gender],
                to_year=date(movie.year, 1, 1))
            ad_r = actor_director_avg_rating(conn, star,
                role_actor_gender[actor.gender],
                director_id, \
                to_year=date(movie.year, 1, 1))
            # TODO: actor-genre rating
        except InputError as e:
            print "{} : {}".format(e.msg, e.expr)
        except SizeError as e:
            print "{} : {} - {}, {}".format(e.msg, e.expr, e.size, e.in_expr)
        except UnknownError as e:
            print "{} : {}, {}".format(e.msg, e.expr, e.in_expr)

        try:
            ag_r = person_genre_avg_rating(conn, star,
                role_actor_gender[actor.gender],
                genres, \
                to_year=date(movie.year, 1, 1))
        except InputError as e:
            print "{} : {}".format(e.msg, e.expr)
        except SizeError as e:
            print "{} : {} - {}, {}".format(e.msg, e.expr, e.size, e.in_expr)
        except UnknownError as e:
            print "{} : {}, {}".format(e.msg, e.expr, e.in_expr)

        a_rs[index], ad_rs[index], ag_rs[index] = a_r, ad_r, ag_r

    for i in xrange(0, 3):
        movie_vec += [a_rs[i][0], ad_rs[i][0],
                      ag_rs[i][0]]  # for 1st-3rd stars: add feat for each one.
    movie_vec += [combine_avg(a_rs[3:6])] + [combine_avg(ad_rs[3:6])] + [
        combine_avg(ag_rs[3:6])]  # the avg for 4th-6th
    movie_vec += [combine_avg(a_rs[6:10])] + [combine_avg(ad_rs[6:10])] + [
        combine_avg(ag_rs[6:10])]  # the avg for 4th-6th

    filler = []
    for i in xrange(num_of_stars, 10):
        filler += [None, None]

    movie_vec += filler
    return movie_vec


def _get_movie_stars_w(conn, movie_id):
    stars = []
    try:
        stars = get_movie_stars(conn, movie_id)
    except InputError as e:
        print "{} : {}".format(e.msg, e.expr)
    except UnknownError as e:
        print "In the movie {}, there is (for some reason) {} stars".format(
            e.in_expr, e.expr)
    return stars
