__author__ = 'Yonatan'

import imdb_sql_consts as imdb_sql_consts
from imdb_consts import \
    InputError, DB_DATE, movie_role, info_type, movie_genres
from y_queries import dream_queries
from Movie import Movie
from coefficients_guess import calc_smart_avg
#from generate_actor_data_csvs import AvgMaker
from numpy import nan

YEAR_OPT_COEF = [0.55,0.3,0.1,0.05]

CREW = [
    "director", "writer", "composer"
]


#------------------------------------------------------------------------------
# Utils Functions
#------------------------------------------------------------------------------ 

class AvgMaker(object):
    """Average Calculator"""
    def __init__(self, items=[], are_float = False):
        if len(items) > 0:
             nums = [item if are_float else float(item) for item in items]
             self.sum = sum(nums)
             self.n = len(items)
        else:
            self.sum = 0
            self.n = 0
    def add(self, item, is_float=False):
        self.sum += float(item) if not is_float else item
        self.n += 1
    def avg(self):
        return nan if self.n == 0 else format(self.sum/self.n, '.2f')

def _fetch_query_dream(imdb, query_name, *args):
    return imdb.conn.fetch_query(dream_queries[query_name], *args)


def mat_to_list(mat):
    return mat # temp


def get_person_movies(imdb, id, role):
    # Should be later from a Person Dictionary
    movies_ids = mat_to_list(_fetch_query_dream(imdb, "person movies", id, role))
    movies = [Movie(imdb,id[0]) for id in movies_ids]
    return movies


def get_due_movies(imdb, ids, roles):
    if len(ids)!=2 or len(roles)!= 2:
        raise InputError([ids,roles], "ids and roles size should be 2")
    movies_ids = mat_to_list(_fetch_query_dream(imdb, "due movies", *(ids+roles)))
    movies = [Movie(imdb, id) for id in movies_ids]
    return movies

 
def get_info (imdb, person_id, info):
    # TODO: Error handler: no info
    # TODO: change the info query ?
    #return _fetch_query_dream(imdb, "person info", person_id, info_type[info])
    return nan


def date_to_age(date, to_year=DB_DATE):
    return -1 #TODO: make function


def person_gender(imdb, id):
    return _fetch_query_dream(imdb, "person gender", id)[0][0]


def get_years_of_career(imdb, movies, current_year):
    min_year = current_year
    for movie in movies:
        if movie['year'] < min_year:
            min_year = movie['year']
    return current_year-min_year


def string_out_of_list(list):
    return ', '.join(['%s'%item for item in list])


#------------------------------------------------------------------------------
# Average Function
#------------------------------------------------------------------------------ 

def smart_year_avg(movies, year):
    recent_avg = AvgMaker()
    few_avg = AvgMaker()
    several_avg = AvgMaker()
    many_avg = AvgMaker()
    for movie in movies:
        years_before = year - movie['year']
        if years_before < 2:
            recent_avg.add(movie['rating'])
        elif years_before < 5:
            few_avg.add(movie['rating'])
        elif years_before < 9:
            several_avg.add(movie['rating'])
        else:
            many_avg.add(movie['rating'])
    return calc_smart_avg(YEAR_OPT_COEF,
     [item.avg() for item in [recent_avg, few_avg, several_avg, many_avg]])


def regular_avg(movies):
    avg = AvgMaker()
    for movie in movies: avg.add(movie['rating'])
    return avg.avg()


def avg_rating(imdb, movies, to_year):
    #TODO: change to Movie io Movie

    # delete the movies that is not before this one
    for movie in movies:
        if movie['year'] >= to_year:
            movies.remove(movie)
    # TODO: change avg function
    return regular_avg(movies)


#------------------------------------------------------------------------------
# Features Functions
#------------------------------------------------------------------------------ 

def person_avg_rating(imdb, id, role, to_year=DB_DATE):
    movies = get_person_movies(imdb, id, role)
    return avg_rating(imdb, movies, to_year)


def persons_avg_rating(imdb, ids, roles, to_year=DB_DATE):
    if len(ids) != len(roles):
        raise InputError([ids, roles], "ids and roles size are not the same")
    movies = [
    get_person_movies(imdb, id, role) for (id,role) in zip(ids,roles)] 
    return avg_rating(imdb, movies, to_year)


def due_avg_movies(imdb, ids, roles, to_year=DB_DATE):
    movies = get_due_movies(imdb, ids, roles)
    return avg_rating(imdb, movies, to_year)


#------------------------------------------------------------------------------
# Feature Vector Functions
#------------------------------------------------------------------------------ 

def bin_genre_feats(genres):
    genre_feats = []
    for genre in movie_genres:
        genre_feats += ("Is "+genre, 1 if genre in genres else 0)
    return genre_feats

def bin_lang_feats(langs):
    # TODO: this function
    return []

def star_feats(imdb, star, i, director, year):
    feats_names = [
        "Star_%s Age",
        "Star_%s Height",
        "Star_%s Is Male",
        "Star_%s Years of Acting",
        "Star_%s Number of Movies", 
        "Star_%s Avg",
        "Star_%s - Director Avg"
        # Gender??
    ]
    feats_names = [feat_name %i for feat_name in feats_names]

    if star == nan:
        return zip(feats_names,[nan]*len(feats_names))

    star_gender = person_gender(imdb, star)
    role = movie_role["actor"] if star_gender == 'm' else movie_role["actress"]
    print i
    if i==3:
        print "STOP!"
    movies = get_person_movies(imdb, star, role)
    return zip(feats_names, [
            date_to_age(get_info(imdb, star, "birth date")),
            get_info(imdb, star, "height"),
            True if star_gender=='m' else False,
            get_years_of_career(imdb, movies, year),
            len(movies),
            person_avg_rating(imdb, star, role),
            due_avg_movies(imdb, [star, director], [role, movie_role["director"]])
        ])


def get_stars_feats(imdb, stars, director, year):
    stars_feats = []
    for i in xrange(3):
        stars_feats += star_feats(imdb, stars[i], i+1, director, year)
    for i in xrange(3):
        for j in xrange(3):
            if i >= j: break
            stars_feats += ("Stars %s & %s" %(i,j),
            due_avg_movies(imdb, [stars[i],stars[j]], '1,2', year))
    return stars_feats 


def get_general_movie_feats(imdb, movie):
    # TODO: import MPAA and budget
    return [
        ("Year", movie['year']),
        #("MPAA", nan),
        #("Budget", nan),
        ("Runtime", movie['runtimes'])
    ]

def get_crew_avg_feats(imdb, movie):
    return [("%s avg rating"%crew_type,
             person_avg_rating(imdb, string_out_of_list(movie[crew_type+'s']), movie_role[crew_type], movie['year'])
             ) for crew_type in CREW]



def get_movie_features(imdb, movie_id, movie=None):
    if movie == None:
        movie = Movie(imdb, movie_id)
    directors = movie['directors']
    directors_string = string_out_of_list(directors)
    stars = movie['stars']

    return  get_general_movie_feats(imdb, movie) \
          + get_stars_feats(imdb, stars, directors_string, movie['year']) \
          + get_crew_avg_feats(imdb, movie) + bin_genre_feats(movie['genres']) #bin_lang_feats(movie['languages'])
