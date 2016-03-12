__author__ = 'Yonatan'


dream_queries = {
	"person movies": \
		"SELECT movie_id FROM cast_info WHERE person_id IN (%s) AND role_id IN (%s)",
	"actors movies": \
		"SELECT movie_id FROM cast_info WHERE person_id IN (%s) AND role_id IN (1,2)",
	"person movies year": \
		"SELECT * FROM movies_of_stars WHERE star_id = %s",
	"due movies": \
		"SELECT cast_1.movie_id FROM cast_info as cast_1 \
		INNER JOIN cast_info as cast_2 ON cast_1.movie_id = cast_2.movie_id \
		AND cast_1.id != cast_2.id WHERE cast_1.person_id = %s \
		AND cast_2.person_id IN (%s)  AND cast_1.role_id IN (%s) \
		AND cast_2.role_id IN (%s)",
	"person info": 
		"SELECT info FROM person_info WHERE person_id = %s AND info_type_id = %s",
	"person gender": "SELECT gender FROM name WHERE id = %s",
    "actor movies": "SELECT movie_id, actors.index FROM actors WHERE person_id = %s",
    "star movies": "SELECT movie_id, stars.index FROM stars WHERE person_id = %s",
	"movies where acted": "SELECT * FROM actors_movies WHERE person_id = %s",
	"movies where stared": "SELECT * FROM stars_movies WHERE person_id = %s"


}
