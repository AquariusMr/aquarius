"""
pymsql
"""

import contextlib
try:
    import pymysql as mysql
except ImportError:
    raise Exception("need pip3 install pymysql")


class SqlCache(object):
    """cache"""
    def __init__(self):
        self.string = ""
        self.result = None

    def clear(self):
        """clear"""
        self.string = ""
        self.result = None


class MysqlAlready(object):
    """mysql"""

    def __init__(self, *args, **kwargs):
        """*host, *port, *user, *password, *db, charset"""
        self.connect = mysql.connect(*args, **kwargs)
        self.cursor = self.connect.cursor()
        self.cache = SqlCache()

    def connect_close(self):
        self.connect.close()

    def cursor_close(self):
        self.cursor.close()

    def sql(self, sql_string, *args, **kwargs):
        self.cursor.execute(sql_string, *args, **kwargs)

    def sql_cache(self, sql_string=None, *args, **kwargs):

        if sql_string != self.cache.string:
            self.sql(sql_string, *args, **kwargs)
            self.cache.string = sql_string
            self.cache.result = self.cursor.fetchall()
        return self.cache.result

    def sql_commit(self, sql_string, *args, **kwargs):
        self.sql(sql_string, *args, **kwargs)
        self.commit()

    def commit(self):
        self.connect.commit()

    def result(self):
        return self.cursor.fetchall()

    @contextlib.contextmanager
    def __call__(self, *args, **kwargs):
        conn = self.connect
        cursor = conn.cursor(*args, **kwargs)
        try:
            yield cursor
        finally:
            conn.commit()
            cursor.close()
