from imdb import IMDb
from prep.IMDB import IMDB
from prep.settings import DB_URI


def fill_movie_imdbid():
    imdb_conn = IMDb('sql', DB_URI)
    cust_conn = IMDB()

    ids = cust_conn.fetch_vec('SELECT id FROM title WHERE imdb_id IS NULL;')
    for id in ids:
        print id
        imdb_conn.get_imdbMovieID(id)

    cust_conn.execute_query(
            'UPDATE movie,title SET movie.imdb_id=title.imdb_id WHERE title.id=movie.id;')

    cust_conn.execute_query("INSERT INTO missing_movies (SELECT * FROM movie WHERE "
                            "imdb_id IS NULL);")

    cust_conn.execute_query("DELETE FROM movie WHERE imdb_id IS NULL;")


def fill_info():
    imdb_conn = IMDb('sql', DB_URI)
    cust_conn = IMDB()

    ids = cust_conn.fetch_vec('SELECT imdb_id FROM title WHERE NOT imdb_id IS NULL;')
    for id in ids:
        try:
            imdb_conn.get_movie_business(id)
        except:
            print "err %s \n" % id


if __name__ == "__main__":
    fill_movie_imdbid()
    # fill_info()
