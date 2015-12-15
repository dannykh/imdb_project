__author__ = 'Yonatan'


dream_queries = {
	"person movies": \
		"SELECT movie_id FROM cast_info WHERE person_id IN (%s) AND role_id = %s",
	"due movies": \
		"SELECT cast_1.movie_id FROM cast_info as cast_1 \
		INNER JOIN cast_info as cast_2 ON cast_1.movie_id = cast_2.movie_id \
		AND cast_1.id != cast_2.id WHERE cast_1.person_id = %s \
		AND cast_2.person_id IN (%s)  AND cast_1.role_id IN (%s) \
		AND cast_2.role_id IN (%s)",
	"person info": 
		"SELECT info FROM person_info WHERE person_id = %s AND info_type_id = %s",
	"person gender": "SELECT gender FROM name WHERE id = %s"

}
