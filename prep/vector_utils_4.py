from Cython.Compiler.Parsing import p_module

__author__ = 'Yonatan'

import imdb_sql_consts as imdb_sql_consts
from imdb_consts import \
    InputError, DB_DATE, movie_role, info_type, movie_genres
from y_queries import dream_queries
from Movie import Movie
from coefficients_guess import calc_smart_avg
from math import isnan
#from generate_actor_data_csvs import AvgMaker
from numpy import nan

#YEAR_OPT_COEF = [0.55,0.3,0.1,0.05]
YEAR_OPT_COEF = [0.53,0.24,0.15,0.08]
YEAR_ACT_COEF = [0.35, 0.27, 0.23, 0.15]
VOTES_OPT_COEF = [0.05, 0.47, 0.27, 0.21]
IMPOR_OPT_COEF = [0.75, 0.2, 0.05]

CREW = [
    "director", "writer", "composer"
]


#------------------------------------------------------------------------------
# Classes
#------------------------------------------------------------------------------

class movieAvg(object):
    """docstring for smartAvg"""
    def __init__(self, year=DB_DATE, movies=[]):
        self.movies = [] # WHY??
        self.n = len(movies)
        self.year = year

    def add(self, movie):
        self.movies += [movie]
        self.n += 1

    def avg(self):
        return AvgMaker([movie['rating'] for movie in self.movies]).avg()

    def smart_v_avg(self):
        return smart_votes_avg(self.movies, self.year)



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

#------------------------------------------------------------------------------
# Utils Functions
#------------------------------------------------------------------------------

def _fetch_query_dream(imdb, query_name, *args):
    return imdb.conn.fetch_query(dream_queries[query_name], *args)


def mat_to_list(mat):
    return mat # temp


def get_person_movies(imdb, id, role):
    # Should be later from a Person Dictionary
    if role == '1,2':
        movies_ids = mat_to_list(_fetch_query_dream(imdb, "actors movies", id))
    else:
        movies_ids = mat_to_list(_fetch_query_dream(imdb, "person movies", id, role))
    movies = [Movie(imdb,id[0]) for id in movies_ids]
    return movies

def get_actor_movies(imdb, id, role):
    # Should be later from a Person Dictionary
    movies_ids = mat_to_list(_fetch_query_dream(imdb, "actor movies", id))
    movies = [Movie(imdb,id[0]) for id in movies_ids]
    #return zip(movies, [mov[1] for mov in movies_ids]) - IF YOU WANT ORDER...
    return movies

def get_star_movies(imdb, id, role):
    # Should be later from a Person Dictionary
    movies_ids = mat_to_list(_fetch_query_dream(imdb, "star movies", id))
    movies = [Movie(imdb,id[0]) for id in movies_ids]
    #return zip(movies, [mov[1] for mov in movies_ids]) - IF YOU WANT ORDER...
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
    return 1 if _fetch_query_dream(imdb, "person gender", id)[0][0]== 'm' else -1


def get_years_of_career(imdb, movies, current_year):
    min_year = current_year
    for movie in movies:
        if movie['year'] < min_year:
            min_year = movie['year']
    return current_year-min_year


def string_out_of_list(list):
    return ', '.join(['%s'%item for item in list])


def past_movies(movies, to_year=DB_DATE+1):
    p_movs = []
    for movie in movies:
        if movie['year']<to_year:
            p_movs+=[movie]
    return p_movs

#------------------------------------------------------------------------------
# Average Function
#------------------------------------------------------------------------------ 

def smart_year_avg(movies, year,actor=False):
    recent_avg = AvgMaker()
    few_avg = AvgMaker()
    several_avg = AvgMaker()
    many_avg = AvgMaker()
    for movie in movies:
        years_before = year - movie['year']
        if  years_before < 0:
            continue
        if years_before < 2:
            recent_avg.add(movie['rating'])
        elif years_before < 5:
            few_avg.add(movie['rating'])
        elif years_before < 9:
            several_avg.add(movie['rating'])
        else:
            many_avg.add(movie['rating'])
    return calc_smart_avg(YEAR_OPT_COEF if not actor else YEAR_ACT_COEF,
     [item.avg() for item in [recent_avg, few_avg, several_avg, many_avg]])

def smart_votes_avg(movies, year):

    header = ['rating', 'known avg', 'popular avg', "very popular avg"]

    known_avg = AvgMaker() # 5,000 - 50,000
    well_known_avg = AvgMaker()
    popular_avg = AvgMaker() # 50,000 - 500,000
    very_popular_avg = AvgMaker() # 500,000 +
# 50,000 20,000 8500
    for movie in movies:
        if int(movie['year']) >= year: continue
        if   int(movie['votes']) < 8000:
            known_avg.add(movie['rating'])
        elif int(movie['year']) < 20000:
            well_known_avg.add(movie['rating'])
        elif int(movie['year']) < 50000:
            popular_avg.add(movie['rating'])
        else:
            very_popular_avg.add(movie['rating'])
    return calc_smart_avg(VOTES_OPT_COEF,
     [item.avg() for item in [known_avg, well_known_avg, popular_avg, very_popular_avg] ])

'''
    Delete
'''
def smart_y_v_avg(movies, year):
    recent_avg = movieAvg(year=year)
    few_avg = movieAvg(year=year)
    several_avg = movieAvg(year=year)
    many_avg = movieAvg(year=year)
    for movie in movies:
        years_before = year - movie['year']
        if years_before < 2:
            recent_avg.add(movie)
        elif years_before < 5:
            few_avg.add(movie)
        elif years_before < 9:
            several_avg.add(movie)
        else:
            many_avg.add(movie)
    return calc_smart_avg(YEAR_OPT_COEF ,
     [item.smart_v_avg() for item in [recent_avg, few_avg, several_avg, many_avg]])

def regular_avg(movies):
    avg = AvgMaker()
    for movie in movies: avg.add(movie['rating'])
    return avg.avg()


def avg_rating(movies, to_year, smart=False, actor=False):
    #TODO: change to Movie io Movie

    # delete the movies that is not before this one

    # STUPID:
    '''
    for movie in movies:
        if movie['year'] >= to_year:
            movies.remove(movie)
    '''
    movies = past_movies(movies, to_year)
    # TODO: change avg function
    #avg = smart_year_avg(movies, to_year, actor=actor) if smart else regular_avg(movies)
    avg = smart_y_v_avg(movies, to_year)
    #avg = smart_y_v_avg(movies, to_year)
    return avg


#------------------------------------------------------------------------------
# Features Functions
#------------------------------------------------------------------------------ 

def person_avg_rating(imdb, id, role, to_year=DB_DATE):
    movies = get_person_movies(imdb, id, role)
    return avg_rating( movies, to_year, smart=True)

def star_scroe(stared, acted, shown, to_year=DB_DATE):
    avg = nan
    if len(shown)==0:
        stared_avg = float(avg_rating(stared, to_year=to_year))
        acted_avg = float(avg_rating(acted, to_year=to_year))
        if isnan(stared_avg) and isnan(acted_avg):
            avg = nan
        elif isnan(stared_avg):
            avg = format(acted_avg, '.2f')
        elif isnan(acted_avg):
            avg = format(stared_avg, '.2f')
        else:
            avg = format((2.5*stared_avg+acted_avg)/3.5, '.2f')
    else:
        avg = avg_rating(shown, to_year=to_year)
    return avg


def persons_avg_rating(imdb, ids, roles, to_year=DB_DATE):
    if len(ids) != len(roles):
        raise InputError([ids, roles], "ids and roles size are not the same")
    movies = [
    get_person_movies(imdb, id, role) for (id,role) in zip(ids,roles)] 
    return avg_rating( movies, to_year)


def due_avg_movies(imdb, ids, roles, to_year=DB_DATE):
    movies = get_due_movies(imdb, ids, roles)
    return avg_rating( movies, to_year)


#------------------------------------------------------------------------------
# Feature Vector Functions
#------------------------------------------------------------------------------ 

def bin_genre_feats(genres):
    genre_feats = []
    for genre in movie_genres:
        genre_feats += [("Is "+genre, 1 if genre in genres else -1)]
    return genre_feats

def bin_lang_feats(langs):
    # TODO: this function
    return []

def star_feats(imdb, star, i, director_movies, year):
    feats_names = [
        #"Star_%s Age",
        #"Star_%s Height",
        #"Star_%s Is Male",
        #"Star_%s Years of Acting",
        #"Star_%s Number of Movies",
        "Star_%s Smart Avg",
        "Star_%s - Director Smart Avg"
        # Gender??
    ]
    feats_names = [feat_name %i for feat_name in feats_names]

    if star == -1:
        return zip(feats_names,[nan]*len(feats_names))

    try:
        star_gender = person_gender(imdb, star)
        role = movie_role["actor"] if star_gender == 1 else movie_role["actress"]
    except Exception:
        star_gender = 0
        role =  '%s, %s'%(movie_role["actor"], movie_role["actress"])

    stared_movies = past_movies(get_star_movies(imdb, star, role), to_year=year)
    acted_movies = past_movies(get_actor_movies(imdb, star, role), to_year=year)
    if len(stared_movies)==0 and len(acted_movies)==0:
        movies = get_person_movies(imdb, star, role)
    else:
        movies = []
    star_dir_movies = [movie for movie in movies+acted_movies+stared_movies if movie in director_movies and movie['year']<year]
    return zip(feats_names, [
            #date_to_age(get_info(imdb, star, "birth date")),
            #get_info(imdb, star, "height"),
            #star_gender,
            #get_years_of_career(imdb, movies, year),
            #len(movies),
            star_scroe(stared_movies, acted_movies, movies, to_year=year),
            #due_avg_movies(imdb, [star, director], [role, movie_role["director"]])
            avg_rating( star_dir_movies, year, smart=True)
        ])


def get_stars_feats(imdb, stars, director, year):
    stars_feats = []
    stars = (stars+[-1]*3)[0:3]
    director_movies = get_person_movies(imdb, director, movie_role['director'])
    for i in xrange(3):
        stars_feats += star_feats(imdb, stars[i], i+1, director_movies, year)
    for i in xrange(3):
        for j in xrange(3):
            if i >= j: continue
            stars_feats += [("Stars %s & %s" %(i+1,j+1),
            due_avg_movies(imdb, [stars[i],stars[j]], ['1, 2', '1, 2'], year))]
    return stars_feats 


def get_general_movie_feats(imdb, movie):
    # TODO: import MPAA and budget
    return [
        #("Year", movie['year']),
        #("MPAA", nan),
        #("Budget", nan),
        #("Runtime", movie['runtimes'])
    ]

def get_crew_avg_feats(imdb, movie):
    return [("%s smart avg rating"%crew_type,
             person_avg_rating(imdb, string_out_of_list(movie[crew_type+'s']), movie_role[crew_type], movie['year'])
             ) for crew_type in CREW]



def get_movie_features(imdb, movie_id, movie=None):
    if movie == None:
        movie = Movie(imdb, movie_id)
    print movie['title']
    directors = movie['directors']
    directors_string = string_out_of_list(directors)
    stars = movie['stars']

    return get_general_movie_feats(imdb, movie) +\
           get_stars_feats(imdb, stars, directors_string, movie['year']) +\
           get_crew_avg_feats(imdb, movie) #+ bin_genre_feats(movie['genres']) #bin_lang_feats(movie['languages'])

#------------------------------------------------------------------------------
# Temp
#------------------------------------------------------------------------------ 

WITH_PRIO = False

def star_feats_prio(imdb, star, i, director_movies, year):
    feats_names = [
        "Star_%s a Avg",
        "Star_%s s Avg",
        "Star_%s a y Avg",
        "Star_%s s y Avg",
        "Star_%s a- Director Avg",
        "Star_%s s- Director Avg",
        "Star_%s a- Director y Avg",
        "Star_%s s- Director y Avg"

    ]
    feats_names = [feat_name %i for feat_name in feats_names]

    if star == -1:
        return zip(feats_names,[nan]*len(feats_names))

    try:
        star_gender = person_gender(imdb, star)
        role = movie_role["actor"] if star_gender == 1 else movie_role["actress"]
    except Exception:
        star_gender = 0
        role =  '%s, %s'%(movie_role["actor"], movie_role["actress"])

    actor_movies = get_actor_movies(imdb, star, role)
    star_movies = get_star_movies(imdb, star, role)
    star_dir_movies = [movie for movie in star_movies if movie[0] in director_movies and movie[0]['year']<year]
    actor_dir_movies = [movie for movie in actor_movies if movie[0] in director_movies and movie[0]['year']<year]

    if not WITH_PRIO:
        actor_movies = [movie[0] for movie in actor_movies]
        star_movies = [movie[0] for movie in star_movies]
        star_dir_movies = [movie[0] for movie in star_dir_movies]
        actor_dir_movies = [movie[0] for movie in actor_dir_movies]
    return zip(feats_names, [
            avg_rating( actor_movies, year),
            avg_rating( star_movies, year),
            avg_rating( actor_movies, year, smart=True),
            avg_rating( star_movies, year, smart=True),
            avg_rating( actor_dir_movies, year),
            avg_rating( star_dir_movies, year),
            avg_rating( actor_dir_movies, year, smart=True),
            avg_rating( star_dir_movies, year, smart=True)
        ])


def get_stars_feats_prio(imdb, stars, director, year):
    stars_feats = []
    stars = (stars+[-1]*3)[0:3]
    director_movies = get_person_movies(imdb, director, movie_role['director'])
    for i in xrange(3):
        stars_feats += star_feats_prio(imdb, stars[i], i+1, director_movies, year)
    return stars_feats 


def get_stars_avg_prio(imdb, movie_id, movie=None):
    if movie == None:
        movie = Movie(imdb, movie_id)
    print movie['title']
    directors = movie['directors']
    directors_string = string_out_of_list(directors)
    stars = movie['stars']

    return get_stars_feats_prio(imdb, stars, directors_string, movie['year'])