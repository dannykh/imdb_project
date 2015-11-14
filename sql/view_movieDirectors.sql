CREATE VIEW movie_director AS 
SELECT movie_id as id, person_id as director_id 
FROM cast_info WHERE role_id=8