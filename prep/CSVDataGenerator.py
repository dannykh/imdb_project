from data.meta import DataDirControl
from IMDB import IMDB
import os
from MovieVector import MovieVectorError
import traceback
import csv
from datetime import timedelta
from monotonic import monotonic
import pandas
import petl as etl
from sklearn import preprocessing
import numpy as np


class DataFileGenerator(object):
    def __init__(self, imdb_conn=None):

        self.imdb_conn = IMDB() if imdb_conn is None else imdb_conn

    def fix(self, data_version_num=None):
        raise NotImplementedError

    def generate_csv(self, movie_vectorizer, movie_generator=None):
        """
        :param movie_vectorizer: Instance of MovieVectorGenerator
        :param movie_generator: Generator of Movies
        :return: path to data_raw file
        """
        data_dir_ctrl = DataDirControl(str(movie_vectorizer))
        start_time = monotonic()
        data_dir = data_dir_ctrl.create_version()
        with open(data_dir + "about.txt", 'wb') as about_fp:
            about_fp.write("Vector type : {}\n".format(movie_vectorizer))
            about_fp.write(
                "Vector desc : {}\n".format(movie_vectorizer.VECTOR_DESC))
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
            # csv_writer.writerow(range(0, len(movie_vectorizer.VECTOR_FORMAT)))
            for movie in movie_generator:
                total += 1
                try:
                    movie.update()
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

    def generate_normalized(self, data_raw_path, normalizer=None,
            output_path=None):
        if output_path is None:
            output_path = '/'.join(
                data_raw_path.split('/')[:-1] + ["data_normal.csv"])

        # tbl = etl.fromcsv(data_raw_path)
        # tbl_np = np.array(tbl.toarray())

        tbl_np = np.genfromtxt(data_raw_path, dtype=float, delimiter=',')
        # tbl_np_scaled=preprocessing.scale(tbl_np)

        min_max_scalar = preprocessing.MinMaxScaler((-1.0, 1.0))

        tbl_np_scaled = min_max_scalar.fit_transform(X=tbl_np)

        # print(tbl_np_scaled)
        etl.tocsv(tbl_np_scaled, output_path)


from MovieVector_1 import MovieVectorGenerator1
from MovieVector2 import MovieVectorGenerator2


def run():
    imdb = IMDB()
    vectorizer = MovieVectorGenerator2(imdb_conn=imdb)

    gen = DataFileGenerator(imdb)
    path = data_path = gen.generate_csv(vectorizer)
    # path = "../data/MovieVector2/4/data_raw.csv"
    # gen.generate_normalized(path))


if __name__ == "__main__":
    run()