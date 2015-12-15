import cPickle as pck
from IMDB import IMDB
import pandas as pd
from prep.Movie import Movie


def create_movie_db():
    conn = IMDB()
    ids = conn.fetch_vec("SELECT DISTINCT movie_id FROM stars,title "
                         "WHERE movie_id= title.id ORDER BY production_year ASC")

    table = {key: [] for key in Movie._keys}

    for mov_id in ids:
        mov = Movie(conn, mov_id)
        for key in Movie._keys:
            table[key] += [mov[key]]

    df = pd.DataFrame(table)[Movie._keys]
    df.set_index('id')
    df.to_csv('../data/movies.csv')
    df.to_pickle('../data/movies.pkl')


def pickle_simple():
    conn = IMDB()
    ids = conn.fetch_vec("SELECT DISTINCT movie_id FROM stars,title "
                         "WHERE movie_id= title.id ORDER BY production_year ASC")

    all_movies = [dict(Movie(conn, mid)) for mid in ids]
    with open('../data/movies.pkl','wb') as fp:
        pck.dump(all_movies,fp)



if __name__ == "__main__":
    #create_movie_db()
    pickle_simple()