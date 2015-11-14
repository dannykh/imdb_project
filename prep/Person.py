from collections import namedtuple

casting = namedtuple('Casting', ['movie_id', 'role'])

_person_queries = {
    "get basic info by id": "SELECT name, gender FROM name WHERE id = {}",
    "get cast by id": "SELECT * FROM cast_info WHERE person_id = {}"
}


class PersonError(Exception):
    def __init__(self, id, msg):
        self.message = "Person <{}> : ".format(id) + msg


class Person(dict):
    def __init__(self, conn, id, mode=0):
        self.id = id
        self.mode = mode
        self.conn = conn
        person_info_mat = conn.fetch_query(
            _person_queries["get basic info by id"].format(id))
        if len(person_info_mat) == 0:
            raise PersonError(id)
        self.name, self.gender = \
            conn.fetch_query(
                _person_queries["get basic info by id"].format(id))[0]
        '''
        name_line = conn.fetch_query(_person_queries["get basic info by id"].format(id))[0]
        self.name = name_line[1]
        self.gender = name_line[4]
        #cast_mat = conn.fetch_query(_person_queries["get cast by id"].format(id))

        self.filmography=len(cast_mat)*[0]
        for i,line in enumerate(cast_mat):
            self.filmography[i] = [line[2],line[6]]
        '''

    def __repr__(self):
        return "Person id : {0:5}  |  name : {1:20}  |  gender : {2:2}".format(
            self.id, self.name, self.gender)
