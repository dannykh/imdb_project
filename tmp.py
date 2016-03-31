__author__ = 'Danny'

from prep.movie_vector.movievector_y import MovieVectorGenerator_y
from prep.IMDB import IMDB
from prep.Movie import Movie


def test(id='3309523'):
    cn = IMDB()
    mov = Movie(imdb_conn=cn, sql_id=id)
    # gen = MovieVectorGenerator2(imdb_conn=cn)

    # gen = MovieVectorGenerator_y(cn)
    return mov


import sys
import requests
import lxml.html


def try_stars(id='133093'):
    page = requests.get("http://www.imdb.com/title/tt" + id).content
    hxs = lxml.html.document_fromstring(page)

    print "http://www.imdb.com/title/tt" + id
    return [(hxs.xpath('//*[@id="overview-top"]/div[%s]/a/span/text()' % i), i) for i in
        range(1, 7)]


if __name__ == "__main__":
    pass
