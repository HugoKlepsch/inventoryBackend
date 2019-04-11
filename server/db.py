import MySQLdb


class DB(object):
    _db = None

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def _connect(self):
        self._db = MySQLdb.connect(host=self.host,
                                   port=self.port,
                                   user="root",
                                   password="notwaterloo",
                                   dbname="inventorydb")

    def execute(self, *args, **kwargs):
        try:
            cursor = self._db.cursor()
            cursor.execute(*args, **kwargs)
        except(AttributeError, MySQLdb.OperationalError):
            self._connect()
            cursor = self._db.cursor()
            cursor.execute(*args, **kwargs)
        return cursor

    def executemany(self, *args, **kwargs):
        try:
            cursor = self._db.cursor()
            cursor.executemany(*args, **kwargs)
        except(AttributeError, MySQLdb.OperationalError):
            self._connect()
            cursor = self._db.cursor()
            cursor.executemany(*args, **kwargs)
        return cursor

    def commit(self, *args, **kwargs):
        self._db.commit(*args, **kwargs)
