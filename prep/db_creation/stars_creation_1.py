from prep.IMDB import IMDB
from imdb import IMDb
from itertools import permutations
from prep.imdb_consts import PersonError
import sys

reload(sys)
sys.setdefaultencoding('utf8')  # to prevent all kinds of bugs


def normalize_canonical_name(name):
    name_vec = name.split(',')
    if len(name_vec) <= 2:
        return name
    name = name_vec[len(name_vec) - 2] + "," + name_vec[len(name_vec) - 1]
    return name[1:]


def normalize_name(name):
    name_vec = name.split(' ')
    name = name_vec[1]
    for p in name_vec[2:len(name_vec)]:
        name += " " + p
    name += ", " + name_vec[0]
    return name


def try_name_permutations(name):
    name_vec = name.split(',')
    name_vec = name_vec[0].split(' ') + name_vec[1].split(' ')
    name_vec.remove('')
    for perm in permutations(name_vec):
        # hyph=next(i for i in xrange(0,len(name_vec)) if name_vec[i]==',')
        for hyph in xrange(1, len(name_vec)):
            yield ' '.join(perm[0:hyph]) + ', ' + ' '.join(
                perm[hyph:len(name_vec)])


def get_actor_sql_id(http_conn, imdb, actor):
    http_conn.update(actor)
    name = actor['canonical name']
    index = -1
    if actor.has_key('imdbIndex'):
        index = actor['imdbIndex']
    try:
        id = imdb.search_person(name, index)
        return id
    except IndexError, e:
        for name_opt in try_name_permutations(name):
            try:
                id = imdb.search_person(name_opt, index)
                return id
            except IndexError, e2:
                {}


def process_movie(http_conn, imdb, movie, log_fp, fail_fp, id):
    max_id = id
    try:
        imdb_movie = \
            http_conn.search_movie(movie.title + " ({})".format(movie.year))[0]
        http_conn.update(imdb_movie)
        cast = imdb_movie['cast'][:10]
        stars = []
        for index, actor in enumerate(cast, 1):
            try:
                imdb_person_id = get_actor_sql_id(http_conn, imdb, actor)
                if imdb_person_id is None:
                    raise PersonError('')
                stars.append((movie.id, imdb_person_id, index))
            except Exception, e2:
                log_fp.write(" {} AT < {} > MOVIE ID {} \n".format(e2.message,
                                                                   actor[
                                                                       "name"],
                                                                   movie.id))
        for star in stars:
            q = 'INSERT INTO stars_temp VALUES ({},{},{},{});'.format(max_id,
                                                                      *star)
            res_id = imdb.execute_query(q)
            max_id = max(max_id, res_id + 1)
    except Exception, eg:
        fail_fp.write("{}\n".format(movie.id))
        log_fp.write(
            " MAJOR {} AT MOVIE ID {} \n".format(eg.message, movie.id))

    return max_id


def process_all_movies():
    http_conn = IMDb()
    imdb = IMDB()
    movies_query = "SELECT id FROM title WHERE id NOT IN " \
                   "(SELECT movie_id from stars_temp);"
    query_max_id = "SELECT MAX(id) from stars_temp ;"
    id = imdb.fetch_scalar(query_max_id)[0]
    if id is None:
        id = 0
    id += 1
    with open("stars_log.txt", 'wb', 0) as log, open("stars_failed", 'wb',
                                                     0) as fail_fp:
        for movie in imdb.get_all_movies(movies_query):
            print movie
            id = process_movie(http_conn, imdb, movie, log, fail_fp, id)


def process_missing_movies():
    http_conn = IMDb()
    imdb = IMDB()
    query_max_id = "SELECT MAX(id) from stars_temp ;"
    id = imdb.fetch_scalar(query_max_id)[0]
    if id is None:
        id = 0
    id += 1
    with open("stars_failed", 'r') as fptr, open("stars_log_2.txt", 'wb',
                                                 0) as log_fp, \
            open("stars_failed_2.txt", 'wb', 0) as fail_fp:
        for line in fptr:
            movie = imdb.get_movie(line)
            print movie
            id = process_movie(http_conn,imdb,movie,log_fp,fail_fp,id)


if __name__ == "__main__":
    process_all_movies()
    #process_missing_movies()
