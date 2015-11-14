SELECT rating,`index` FROM movie_year_rating,stars_temp 
WHERE stars_temp.person_id= '1454832'
AND movie_year_rating.id=stars_temp.movie_id AND `index`<=5 
#AND 2000 <= movie_year_rating.year < 2012

# AL pacino : '1454832'