__author__ = 'Danny'

import MySQLdb as sql


class SQLconnection():
    def __init__(self, host, uname, password, dbname):
        self.db = None
        self.host = host
        self.uname = uname
        self.password = password
        self.dbname = dbname
        self.cursor = None

    def connect(self):
        self.db = sql.connect(self.host, self.uname, self.password, self.dbname,
            read_default_file='C:\ProgramData\MySQL\MySQL Server 5.7\my.cnf')
        self.cursor = self.db.cursor()

    def disconnect(self):
        self.db.close()

    def execute_delete_query(self, query, *args):
        self.cursor.execute(query, args)
        self.db.commit()

    def execute_query(self, query, *args):
        self.cursor.execute(query, args)
        #print self.cursor._last_executed
        return self.cursor.lastrowid

    def fetch_query(self, query, *args):
        self.execute_query(query, *args)
        return self.cursor.fetchall()

    def fetch_vec(self, query, *args):
        res = self.fetch_query(query, *args)
        for x in res:  # In case of unnecessary tuples
            if len(x) > 1:
                return res
        return [x[0] for x in res]

    def fetch_scalar(self, query, *args):
        """""
        Returns a scalar result of SELECT query. A tuple.
        """""
        res = self.fetch_vec(query, *args)
        if res:
            return res[0]
        else:
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
