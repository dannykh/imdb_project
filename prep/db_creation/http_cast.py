from prep.IMDB import IMDB
from imdb import IMDb
from prep.imdb_consts import PersonError
from utils import get_sql_id_by_name_in_movie
import sys
import traceback

reload(sys)
sys.setdefaultencoding('utf8')  # prevent all kinds of bugs


def get_actor_sql_id(conn, http_conn, actor, movie_id):
    return get_sql_id_by_name_in_movie(conn, actor['name'], movie_id, roles=(1, 2))


def process_movie(http_conn, imdb, movie, log_fp, fail_fp):
    try:
        imdb_movie = http_conn.get_movie(movie['imdb id'])
        cast = imdb_movie['cast'][:10]
        stars = []
        for index, actor in enumerate(cast, 1):
            try:
                person_id = get_actor_sql_id(imdb, http_conn, actor, movie['id'])
                if person_id is None:
                    raise PersonError('')
                stars.append((movie['id'], person_id, index))
            except Exception, e2:
                log_fp.write(" {} AT < {} > MOVIE ID {} \n".format(e2.message,
                        actor["name"], movie['id']))
        for star in stars:
            q = 'INSERT INTO actors (movie_id,person_id,`index`) ' \
                'VALUES (%s,%s,%s);'
            imdb.execute_query(q, *star)
    except Exception, eg:
        fail_fp.write("{}\n".format(movie['id']))
        log_fp.write(
                " Error {} AT MOVIE ID {} \n {} \n".format(eg.message, movie['id'],
                        traceback.format_exc()))


def process_all_movies():
    http_conn = IMDb()
    imdb = IMDB()
    movies_query = "SELECT id,imdb_id FROM movie WHERE id NOT IN " \
                   "(SELECT distinct movie_id from actors);"
    with open("http_cast_log.txt", 'wb', 0) as log, open("http_cast_failed.txt", 'wb',
            0) as fail_fp:
        for rec in imdb.fetch_vec(movies_query):
            movie = {'id': rec[0], 'imdb id': rec[1]}
            process_movie(http_conn, imdb, movie, log, fail_fp)


import csv


def generate_csv():
    conn = IMDB()
    movies = conn.fetch_vec('SELECT id, imdb_id FROM movie;')
    with open('actors.csv', 'wb', 0) as fp:
        writer = csv.writer(fp)
        for sql_id, imdb_id in movies:
            actors = conn.fetch_vec("SELECT person_id FROM actors "
                                    "WHERE movie_id = %s ORDER BY `index` ASC ;", sql_id)
            writer.writerow([imdb_id] + actors)


def fill_actors(actors_csv='http_linkers/actors.csv'):
    conn = IMDB()
    conn.execute_query('DELETE FROM actors;')
    with open(actors_csv, 'rb') as fp:
        reader = csv.reader(fp)
        for row in reader:
            for index, actor_id in enumerate(row[1:], 1):
                q = 'INSERT INTO actors (movie_id,person_id,`index`) ' \
                    'VALUES (%s,%s,%s);'
                conn.execute_query(q, row[0], actor_id, index)


if __name__ == "__main__":
    # process_all_movies()
    # generate_csv()
    fill_actors()
