from prep.SQLconnection import SQLconnection
import prep.settings as db
from prep.imdb_sql_consts import info_type

delete_queries = [
    "DELETE FROM title WHERE kind_id != 1;",
    "DELETE FROM movie_info_idx WHERE info_type_id NOT IN {} ;".format(tuple(
        tp for tp in info_type.values())),
    "DELETE FROM movie_info WHERE info_type_id NOT IN {} ;".format(tuple(
        tp for tp in info_type.values())),
    "DELETE FROM title WHERE id NOT IN (SELECT movie_id FROM movie_info_idx "
    "WHERE info_type_id=100 AND info >= {});".format(db.MIN_VOTES_FOR_MOVIE),
    "DELETE FROM cast_info WHERE movie_id NOT IN (SELECT id FROM title);",
    "DELETE FROM name WHERE id NOT IN (SELECT person_id FROM cast_info);",
    "DELETE FROM movie_info WHERE movie_id NOT IN (SELECT id FROM title);",
    "DELETE FROM movie_info_idx WHERE movie_id NOT IN (SELECT id FROM title);"
]

optimize_queries = [
    "OPTIMIZE TABLE title;",
    "OPTIMIZE TABLE cast_info;",
    "OPTIMIZE TABLE person;",
    "OPTIMIZE TABLE movie_info;",
    "OPTIMIZE TABLE movie_info_idx;"

]

outdated = [
    "CREATE TABLE `imdb`.`movie_info_all` ("
    "`id` INT(11) NOT NULL AUTO_INCREMENT,"
    "`movie_id` INT(11) NOT NULL,"
    "`info_type_id` INT(11) NOT NULL,"
    "`info` TEXT NOT NULL,"
    "`note` TEXT NULL DEFAULT NULL,"
    "PRIMARY KEY (`id`))"
    "ENGINE = MyISAM;"
]

table_creation = [

    "CREATE TABLE `imdb`.`movies` ("
    "`id` INT(11) NOT NULL,"
    "`title` TEXT NOT NULL,"
    "`production_year` INT(11) NOT NULL,"
    "`imdb_index` VARCHAR(12) NULL DEFAULT NULL,"
    "`rating` TEXT NOT NULL,"
    "`votes` TEXT NOT NULL,"
    "PRIMARY KEY (`id`))"
    "ENGINE = MyISAM;"

]

table_fill = [
    "INSERT INTO movie_info_all SELECT * FROM movie_info;",
    "INSERT INTO movie_info_all SELECT * FROM movie_info_idx;",
    "INSERT INTO movies SELECT title.id,title,production_year,imdb_index,m1.info, m2.info"
    " FROM title,movie_info_idx as m1,movie_info_idx as m2 "
    "WHERE title.id= m1.movie_id AND title.id=m2.movie_id "
    "AND m1.info_type_id=101 AND m2.info_type_id=100;"
]


def run_queries(conn, queries):
    for q in queries:
        print q
        try:
            conn.execute_delete_query(q)
        except Exception, e:
            print "^ NOT EXECUTED"


if __name__ == "__main__":
    conn = SQLconnection(db.DB_HOST, db.DB_USER, db.DB_PSW, db.DB_NAME)
    conn.connect()

    """
    run_queries(conn,delete_queries)
    run_queries(conn,optimize_queries)

    run_queries(conn,table_creation)

    run_queries(conn, table_fill)
    """

conn.disconnect()
