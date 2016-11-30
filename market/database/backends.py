from os import path

from market.dispersy.database import Database


class Backend(object):
    def get(self, type, id):
        raise NotImplementedError

    def post(self, type, id, obj):
        raise NotImplementedError

    def put(self, type, id, obj):
        raise NotImplementedError

    def delete(self, id):
        raise NotImplementedError

    def id_available(self, id):
        raise NotImplementedError

    def exists(self, type, id):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError


class MemoryBackend(Backend):
    _data = {}
    _id = {}

    def get(self, type, id):
        try:
            return self._data[type][id]
        except:
            raise IndexError

    def post(self, type, id, obj):
        if type not in self._data:
            self._data[type] = {}

        if not self.id_available(id):
            raise IndexError("Index already in use")

        self._data[type][id] = obj
        self._id[id] = True

    def put(self, type, id, obj):
        if self.exists(type, id):
            self._data[type][id] = obj
            return True
        return False

    def delete(self, id):
        raise NotImplementedError

    def id_available(self, id):
        return id not in self._id

    def exists(self, type, id):
        if type in self._data:
            return id in self._data[type]
        return False

    def clear(self):
        self._data = {}
        self._id = {}


class PersistentBackend(Database, Backend):
    # Path to the database location + dispersy._workingdirectory
    DATABASE_PATH = u"market.db"
    # Version to keep track if the db schema needs to be updated.
    LATEST_DB_VERSION = 1
    # Schema for the MultiChain DB.
    schema = u"""
    CREATE TABLE IF NOT EXISTS market(
     id		                    TEXT NOT NULL,
     type_name		            TEXT NOT NULL,
     value                      TEXT NOT NULL,

     insert_time                TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
     );

    CREATE TABLE option(key TEXT PRIMARY KEY, value BLOB);
    INSERT INTO option(key, value) VALUES('database_version', '""" + str(LATEST_DB_VERSION) + u"""');
    """

    def __init__(self, working_directory):
        super(PersistentBackend, self).__init__(path.join(working_directory, self.DATABASE_PATH))

    def open(self, initial_statements=True, prepare_visioning=True):
        return super(PersistentBackend, self).open(initial_statements, prepare_visioning)

    def close(self, commit=True):
        return super(PersistentBackend, self).close(commit)

    def check_database(self, database_version):
        assert isinstance(database_version, unicode)
        assert database_version.isdigit()
        assert int(database_version) >= 0
        database_version = int(database_version)

        if database_version < self.LATEST_DB_VERSION:
            # Remove all previous data, since we have only been testing so far, and previous blocks might not be
            # reliable. In the future, we should implement an actual upgrade procedure
            self.executescript(self.schema)
            self.commit()

        return self.LATEST_DB_VERSION

    def get(self, type, id):
        db_query = u"SELECT value FROM `market` WHERE type_name = ? AND id = ?"
        db_result = self.execute(db_query, (unicode(type), unicode(id))).fetchall()

        if len(db_result) != 1:
            raise IndexError

        return db_result[0][0]

    def post(self, type, id, obj):
        if not self.id_available(id):
            raise IndexError("Index already in use")

        db_query = u"INSERT INTO `market` (id, type_name, value) VALUES (?, ?, ?)"
        self.execute(db_query, (unicode(id), unicode(type), unicode(obj)))
        self.commit()

    def put(self, type, id, obj):
        if self.exists(type, id):
            db_query = u"UPDATE `market` SET value = ? WHERE id = ? AND type_name = ?"
            self.execute(db_query, (unicode(obj), unicode(id), unicode(type)))
            self.commit()
            return True
        else:
            return False

    def delete(self, id):
        db_query = u"DELETE FROM `market` WHERE id = ?"
        self.execute(db_query, (unicode(id),))
        self.commit()

    def id_available(self, id):
        db_query = u"SELECT COUNT(*) FROM `market` WHERE id = ?"
        db_result = self.execute(db_query, (unicode(id),)).fetchall()
        return db_result[0][0] == 0

    def exists(self, type, id):
        db_query = u"SELECT COUNT(*) FROM `market` WHERE id = ? AND type_name = ?"
        db_result = self.execute(db_query, (unicode(id), unicode(type))).fetchall()
        return db_result[0][0] == 1

    def clear(self):
        self.execute(u"DELETE FROM market")