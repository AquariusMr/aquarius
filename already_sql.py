import pymysql as mysql

class ExecuteResult(object):

    def __init__(self):
        self.query_string = ""
        self.result = None


class Already(object):

    def __init__(self, *args, **kwargs):

        if not (args and kwargs):
            self.con = self.connect("127.0.0.1", "root", "mysql", "ip")
        else:
            self.con = self.connect(*args, **kwargs)

        if self.auto_commit:
            self.con.autocommit(1)

        self.cur = self.con.cursor()

        self.query_string = ""
        self._result = ExecuteResult()

    @property
    def connect(self):
        return mysql.connect

    @property
    def auto_commit(self):
        return True

    def sql(self, sql=None, *args, **kwargs):
        self.query_string = sql

        if sql[0] != "s":
            self.cur.execute(sql, *args, **kwargs)
            self._result.query_string = sql
            self._result.result = None

        elif self.query_string != self._result.query_string and self._result.result is None:
            self.cur.execute(sql, *args, **kwargs)
            self._result.query_string = sql
            self._result.result = self.cur.fetchall()

        return self._result.result

    def __str__(self):
        return str(self._result.result)
