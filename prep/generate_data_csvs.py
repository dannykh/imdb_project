__author__ = 'Danny'

import csv

from IMDB import IMDB
from imdb_consts import PersonError
from utils import vec_for_movie

file_index = 4
dbname = "imdb_3"

data_set_fname = "data_{}.csv".format(file_index)
binary_tags_fname = "bin_tags_{}.csv".format(file_index)
real_tags_fname = "real_tags_{}.csv".format(file_index)
log_fname = "log_{}.txt".format(file_index)

# Threshold for classifying a movie as "good"
movie_rating_threshold = 8.0

imdb = IMDB(dbname=dbname)


def movie_to_csv(movie, data_fp, bintags_fp, realrags_fp, log_fp):
    data_line = vec_for_movie(imdb, movie.id, movie)
    real_tag = movie.get_rating()
    bin_tag = 0
    if real_tag >= movie_rating_threshold:
        bin_tag = 1

    data_writer.writerow(data_line)
    bintag_writer.writerow([bin_tag])
    realtag_writer.writerow([real_tag])


with open(data_set_fname, 'wb', 0) as data_fp, \
        open(binary_tags_fname, 'wb', 0) as bintags_fp, \
        open(real_tags_fname, 'wb', 0) as realrags_fp, \
        open(log_fname, 'wb', 0) as log_fp,\
        open("missing_movies.txt",'wb',0) as missing_fp:
    movie_count = 0
    error_count = 0
    data_writer = csv.writer(data_fp)
    bintag_writer = csv.writer(bintags_fp)
    realtag_writer = csv.writer(realrags_fp)

    for movie in imdb.get_all_movies():
        try:
            movie_to_csv(movie,data_fp,bintags_fp,realrags_fp,log_fp)
            movie_count += 1

        except PersonError, pe:
            """
            try:
                process_movie(movie,log_fp)
                movie_to_csv(movie,data_fp,bintags_fp,realrags_fp,log_fp)
                movie_count += 1
                log_fp.write("++ FIXED MOVIE {}\n".format(movie.id))
            except Exception, e:
                error_count += 1
                """
            missing_fp.write("{}\n".format(movie.id))

        except Exception, e:
            error_count += 1
            log_fp.write("{} in movie id {} \n".format(e, movie.id))

    print("Finished with {} movies and {} errors ".format(movie_count,
                                                          error_count))
