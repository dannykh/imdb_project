CREATE VIEW MovieYearRating AS 
SELECT title.id AS id,title.production_year AS year,info AS rating
FROM title,movie_info_idx WHERE title.id = movie_id AND info_type_id=101;

