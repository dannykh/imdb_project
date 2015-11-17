import queries_2
import imdb_sql_consts as consts
from numpy import average
from MovieVector import MovieVectorError


def get_all_genres(imdb_conn):
    return imdb_conn.fetch_vec(queries_2.genre['all_genres'])


def actor_movie_average(imdb_conn, actor_id,
        from_year=consts.MIN_YEAR, to_year=consts.DB_YEAR,
        top_k=10, weights=None):
    if weights is None:
        weights = [1.0] * top_k

    actor_ratings = imdb_conn.fetch_vec(
        queries_2.actor['star_rating_index'], actor_id, from_year,
        to_year)
    return average([float(x[0]) * weights[x[1]] for x in actor_ratings])


def director_average(imdb_conn, director_id,
        from_year=consts.MIN_YEAR, to_year=consts.DB_YEAR):
    return imdb_conn.fetch_scalar(queries_2.director['simple_avg'],
        director_id, from_year, to_year)


def get_genre_vec(movie, all_genres=None, conn=None):
    if all_genres is None:
        if conn is None:
            raise MovieVectorError("Bad params")
        all_genres = get_all_genres(conn)
    return map(lambda genre: 1.0 if genre in movie.get_genres() else -1.0,
        all_genres)


def get_feature_subvector(data_generator, data_transformer, expected_len,
        data_param_name, **args):
    len = 0
    feat_vec = []
    for item in data_generator:
        feat_vec += data_transformer(args)
