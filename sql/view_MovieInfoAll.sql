CREATE VIEW movie_info_all as 
SELECT * FROM movie_info 
UNION 
SELECT * FROM movie_info_idx; 