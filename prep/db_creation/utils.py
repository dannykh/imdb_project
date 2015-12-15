from itertools import permutations


def get_name_sql_regex(name):
    name_vec = name.split(' ')
    perms = []
    for perm in permutations(name_vec):
        perms += [u'(.*)' + u'(.*)'.join(perm) + u'(.*)']

    return u'|'.join(perms)


def get_sql_id_by_name_in_movie(conn, name, movie_id, roles=None):
    if not roles is None:
        query = "SELECT id FROM name " \
                "WHERE id IN " \
                "(	SELECT person_id FROM cast_info " \
                "	WHERE movie_id = %s " \
                "   AND role_id IN %s" \
                ")" \
                "AND name REGEXP %s ;"

        return conn.fetch_scalar(query, movie_id, roles, get_name_sql_regex(name))

    else:
        query = "SELECT id FROM name " \
                "WHERE id IN " \
                "(	SELECT person_id FROM cast_info " \
                "	WHERE movie_id = %s )" \
                "AND name REGEXP %s ;"

        return conn.fetch_scalar(query, movie_id, roles, get_name_sql_regex(name))
