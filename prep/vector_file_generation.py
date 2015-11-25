from data.meta import DataDirControl
from IMDB import IMDB
import os
from MovieVector import MovieVectorError
import traceback
import csv
from datetime import timedelta
from monotonic import monotonic
import pandas as pd
import numpy as np


class DataFileGenerator(object):
    def __init__(self, imdb_conn=None):

        self.imdb_conn = IMDB() if imdb_conn is None else imdb_conn

    def fix(self, data_version_num=None):
        raise NotImplementedError

    def generate_csv(self, movie_vectorizer, movie_generator=None,
            limit=None):
        """
        :param movie_vectorizer: Instance of MovieVectorGenerator
        :param movie_generator: Generator of Movies
        :return: path to data_raw file
        """
        if limit is None:
            limit = 999999
        data_dir_ctrl = DataDirControl(str(movie_vectorizer))
        start_time = monotonic()
        data_dir = data_dir_ctrl.create_version()
        with open(data_dir + "about.txt", 'wb') as about_fp:
            about_fp.write("db : {}\n".format(self.imdb_conn.db))

        if movie_generator is None:
            movie_generator = self.imdb_conn.get_all_movies()

        succ_num = 0
        fail_num = 0
        total = 0

        with open(data_dir + "log.txt", 'wb', 0) as log_fp, \
                open(data_dir + "failed.txt", 'wb', 0) as fail_fp, \
                open(data_dir + "data_raw.csv", 'wb', 0) as data_fp:
            csv_writer = csv.writer(data_fp)
            csv_writer.writerow(movie_vectorizer.header)
            for movie in movie_generator:
                if limit <= 0:
                    break
                limit -= 1
                total += 1
                try:
                    movie.update_fields()
                    movie_vec = movie_vectorizer.get_vector(movie)
                    csv_writer.writerow(movie_vec)
                    succ_num += 1
                except Exception, e:
                    fail_num += 1
                    log_fp.write(" {} : <{}> \n {} \n".format(movie.id, e,
                        traceback.format_exc()))
                    fail_fp.write(str(movie.id) + "\n")

        end_time = monotonic()
        with open(data_dir + "about.txt", 'ab') as res_fp:
            res_fp.writelines(["\n",
                "Runtime : {}\n".format(
                    timedelta(seconds=end_time - start_time)),
                "total movies : {}\n".format(total),
                "Success count : {} \n".format(succ_num),
                "Fail count : {} \n".format(fail_num)])
        print "DONE"
        return data_dir + "data_raw.csv"


from MovieVector_1 import MovieVectorGenerator1
from MovieVector2 import MovieVectorGenerator2
from MovieVector3 import MovieVectorGenerator3
from MovieVector_y import MovieVectorGenerator_y

movie_vec_ver = MovieVectorGenerator_y


def run():
    imdb = IMDB()
    vectorizer = movie_vec_ver(imdb_conn=imdb)

    gen = DataFileGenerator(imdb)
    limit = None
    gen.generate_csv(vectorizer, limit=limit)
    # path = data_path = gen.generate_csv(vectorizer)


if __name__ == "__main__":
    run()
