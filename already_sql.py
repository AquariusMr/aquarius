import pymysql as mysql


class SqlCache(object):

    def __init__(self):
        self.string = ""
        self.result = None

    def clear(self):
        self.query_string = ""
        self.query_result = None


class MysqlAlready(object):

    def __init__(self, *args, **kwargs):
        self.connect = mysql.connect(*args, **kwargs)
        self.cursor = self.connect.cursor()
        self.query_cache = SqlCache()

    def sql(self, sql_string=None, *args, **kwargs):

        if sql_string != self.query_cache.string:
            self.exec(sql_string, *args, **kwargs)
            self.query_cache.string = sql_string
            self.query_cache.result = self.cursor.fetchall()

        return self.query_cache.result

    def exec(self, sql_string, *args, **kwargs):
        self.cursor.execute(sql_string, *args, **kwargs)

    def result(self):
        return self.cursor.fetchall()