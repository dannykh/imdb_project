__author__ = 'Danny'

from prep.MovieVector_y import MovieVectorGenerator_y

from prep.IMDB import IMDB
from prep.SqlMovie import SqlMovie


def test(id='3062729'):
    cn = IMDB()
    mov = SqlMovie(imdb_conn=cn, sql_id=id, mode=1)
    # gen = MovieVectorGenerator2(imdb_conn=cn)
    mov.update()

    gen = MovieVectorGenerator_y(cn)
    return gen.get_vector(mov)


if __name__ == "__main__":
    pass