from prep.SQLconnection import SQLconnection
import prep.settings as db

delete_queries = [
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


def clean_db():
    conn = SQLconnection(db.DB_HOST, db.DB_USER, db.DB_PSW, db.DB_NAME)
    conn.connect()
    for q in delete_queries:
        print q
        conn.execute_delete_query(q)

    for q in optimize_queries:
        conn.execute_delete_query(q)

    conn.disconnect()


if __name__ == "__main__":
    clean_db()
