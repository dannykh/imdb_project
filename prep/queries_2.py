stars = {
    "star_rating_index": "SELECT rating,`index` "
                         "FROM movie_year_rating,stars_temp "
                         "WHERE stars_temp.person_id= %s "
                         "AND movie_year_rating.id=stars_temp.movie_id "
                         "AND `index`<=5 "
                         "AND %s <= movie_year_rating.year "
                         "AND movie_year_rating.year < %s ;",

    "simple_avg_top_k": "SELECT AVG(rating) FROM movie_year_rating,stars_temp"
                        "WHERE movie_year_rating.id=stars_temp.movie_id AND"
                        "`index`<=%(k)s AND stars_temp.person_id=%(id)s;"
}

genre = {
    "all_genres": "SELECT DISTINCT info FROM movie_info WHERE info_type_id=3;",

    "avg_rating": "SELECT AVG(rating),COUNT(rating) FROM movie_year_rating,movie_info_all "
                  "WHERE info_type_id=3 AND movie_year_rating.id=movie_info_all.movie_id "
                  "AND info IN %s "
                  "AND %s < year AND year <= %s;"
}

director = {
    "simple_avg": "SELECT AVG(rating) FROM movie_year_rating,movie_director "
                  "WHERE movie_director.director_id=%s "
                  "AND movie_year_rating.id=movie_director.id "
                  "AND %s <= movie_year_rating.year "
                  "AND movie_year_rating.year < %s ;"
}

actor = {
    "actor_avg": "SELECT AVG(rating) FROM movie_year_rating,cast_info "
                 "WHERE cast_info.person_id= %s AND role_id IN (1,2) "
                 "AND movie_year_rating.id = cast_info.movie_id "
                 "AND %s < movie_year_rating.year "
                 "AND movie_year_rating.year <%s ;",

    "in_genres_avg": "SELECT AVG(rating),COUNT(rating) "
                     "FROM movie_year_rating,movie_info_all,cast_info "
                     "WHERE cast_info.person_id = %s AND info_type_id=3 "
                     "AND cast_info.role_id IN (1,2) "
                     "AND movie_year_rating.id=movie_info_all.movie_id "
                     "AND cast_info.movie_id=movie_year_rating.id "
                     "AND info IN %s AND %s < year AND year <= %s ;"
}

person = {
    "avg_rating": "SELECT AVG(rating),COUNT(rating) FROM movie_year_rating,cast_info "
                  "WHERE cast_info.person_id = %s AND role_id IN %s "
                  "AND movie_year_rating.id=cast_info.movie_id "
                  "AND %s <= movie_year_rating.year AND movie_year_rating.year < %s;",

    "multi_avg_rating": "SELECT AVG(rating),COUNT(rating) FROM movie_year_rating,cast_info "
                        "WHERE cast_info.person_id IN %s AND role_id in %s "
                        "AND movie_year_rating.id=cast_info.movie_id "
                        "AND %s <= movie_year_rating.year AND movie_year_rating.year < %s;",

    "in_genres_avg": "SELECT AVG(rating),COUNT(rating) "
                     "FROM movie_year_rating,movie_info_all,cast_info "
                     "WHERE cast_info.person_id = %s AND info_type_id=3 "
                     "AND cast_info.role_id IN %s "
                     "AND movie_year_rating.id=movie_info_all.movie_id "
                     "AND cast_info.movie_id=movie_year_rating.id "
                     "AND info IN %s AND %s < year AND year <= %s ;"
}

combined = {
    "person-director_avg_rating": "SELECT AVG(rating),COUNT(rating) "
                                  "FROM movie_year_rating "
                                  "WHERE movie_year_rating.id IN ( "
                                  "SELECT c1.movie_id "
                                  "FROM cast_info AS c1 ,cast_info AS c2 "
                                  "WHERE c1.person_id = %s "
                                  "AND c1.role_id IN %s "
                                  "AND c2.person_id = %s "
                                  "AND  c2.role_id=8 "
                                  "AND c1.movie_id = c2.movie_id ) "
                                  "AND %s < year AND year <= %s ;"
}
