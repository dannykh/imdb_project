from prep.db_creation.clean_db import clean
from prep.db_creation.stars import fill_stars
from prep.db_creation.db_http_fillup import fill_movie_imdbid
import time
import http_cast


def setup():
    clean()

    for x in xrange(0, 1):
        fill_movie_imdbid()
        #time.sleep(300)
    fill_stars()

    http_cast.process_all_movies()


if __name__ == "__main__":
    setup()
