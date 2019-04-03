import psycopg2

class DB:
    _db = None

    def _connect(self):
        self._db = psycopg2.connect(host="inventorydb.inventory", 
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
