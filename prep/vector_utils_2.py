import queries_2
import imdb_sql_consts as consts
from numpy import average


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
