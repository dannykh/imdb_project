avg_queries = {
    "person avg rating":
        "SELECT avg(info), COUNT(info) FROM movie_info_idx WHERE "
        "info_type_id = {} AND movie_id IN ("
        "SELECT movie_id FROM cast_info WHERE role_id = {} AND person_id = {} )"
        " AND movie_id IN ("
        "SELECT id FROM title WHERE {} <= production_year AND {} > production_year)",

    "persons avg rating":
        "SELECT avg(info), COUNT(info) FROM movie_info_idx WHERE info_type_id = {}"
        " AND movie_id IN ("
        "SELECT movie_id FROM cast_info WHERE role_id = {} AND person_id IN ({}) ) "
        "AND movie_id IN ("
        "SELECT id FROM title WHERE {} <= production_year AND {} > production_year)",

    "person-director avg rating":
        "SELECT AVG(info), COUNT(info) FROM movie_info_idx WHERE info_type_id = {}"
        " AND movie_id IN ("
        "SELECT movie_id FROM cast_info WHERE role_id = {} AND person_id = {} "
        "AND movie_id IN ("
        "SELECT movie_id FROM cast_info WHERE role_id = {} AND person_id = {})) "
        "AND movie_id IN ("
        "SELECT id FROM title WHERE {} <= production_year AND {} > production_year);",

    "actor in genre avg rating":
        "SELECT AVG(info), COUNT(info) FROM movie_info_idx WHERE info_type_id = {} "
        "AND movie_id IN ("
        "SELECT movie_id FROM cast_info WHERE role_id = {} AND person_id = {} "
        "AND movie_id IN ("
        "SELECT movie_id FROM movie_info WHERE info_type_id = {} AND info = '{}')) "
        "AND movie_id IN ("
        "SELECT id FROM title WHERE {} <= production_year AND {} > production_year);",

    "actor in genres avg rating":
        "SELECT AVG(info), COUNT(info) FROM movie_info_idx WHERE info_type_id = {} "
        "AND movie_id IN ("
        "SELECT movie_id FROM cast_info WHERE role_id = {} AND person_id = {} "
        "AND movie_id IN ("
        "SELECT movie_id FROM movie_info WHERE info_type_id = {} AND info IN ({}) ))"
        " AND movie_id IN ("
        "SELECT id FROM title WHERE {} <= production_year AND {} > production_year);",

    "genre avg rating":
        "SELECT AVG(info), COUNT(info) FROM movie_info_idx WHERE info_type_id = {} "
        "AND movie_id IN ("
        "SELECT movie_id FROM movie_info WHERE info_type_id = {} AND info = '{}') "
        "AND movie_id IN ("
        "SELECT id FROM title WHERE {} <= production_year AND {} > production_year);",

    "genres avg rating":
        "SELECT AVG(info), COUNT(info) FROM movie_info_idx WHERE info_type_id = {} "
        "AND movie_id IN ("
        "SELECT movie_id FROM movie_info WHERE info_type_id = {} AND info IN ({}) )"
        " AND movie_id IN ("
        "SELECT id FROM title WHERE {} <= production_year AND {} > production_year);"
}

get_queries = {
    "movie stars": "SELECT person_id , `index` FROM stars_temp where movie_id = {} "
                   "order by `index`;",
    "movie participant": "SELECT person_id FROM cast_info where movie_id = {} "
                         "AND role_id = {};"
}