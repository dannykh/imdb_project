actor = {
    "star_rating_index": "SELECT rating,`index` "
                         "FROM movie_year_rating,stars_temp "
                         "WHERE stars_temp.person_id= %s "
                         "AND movie_year_rating.id=stars_temp.movie_id "
                         "AND `index`<=5 "
                         "AND %s <= movie_year_rating.year < %s ;",

    "simple_avg_top_k": "SELECT AVG(rating) FROM movie_year_rating,stars_temp"
                        "WHERE movie_year_rating.id=stars_temp.movie_id AND"
                        "`index`<=%(k)s AND stars_temp.person_id=%(id)s;"
}

genre = {
    "all_genres": "SELECT DISTINCT info FROM movie_info WHERE info_type_id=3;"
}

director = {
    "simple_avg": "SELECT avg(rating) FROM movie_year_rating,movie_director "
                  "WHERE movie_director.director_id=%s "
                  "AND movie_year_rating.id=movie_director.id "
                  "AND %s <= movie_year_rating.year < %s;"
}