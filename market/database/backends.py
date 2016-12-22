from os import path

from dispersy.database import Database


class Backend(object):
    """
    The backend interface
    """
    
    def get(self, _type, _id):
        """
        Get an item out of the key value store.
        :param _type: The type name of the value
        :param _id: The id of the value
        :return: The value
        :raises: IndexError if not found
        """
        raise NotImplementedError

    def post(self, _type, _id, obj):
        """
        Save a value to the key value store
        :param _type: The type name of the value
        :param _id: The id of the value
        :param obj: The value
        :return: True if succeeds, IndexError if `_id` already in use.
        """
        raise NotImplementedError

    def put(self, _type, _id, obj):
        """
        Replace a value in the key value store
        :param _type: The type name of the value
        :param _id:  The id of the value
        :param obj: The value
        :return: True if succeeds, False if <type, id> not already in use. (Won't be saved either)
        """
        raise NotImplementedError

    def delete(self, obj):
        """
        Delete a value in the key value store
        :param obj:
        :return:
        """
        raise NotImplementedError

    def id_available(self, _id):
        """
        Check if an ID is available
        :param _id:
        :return:
        """
        raise NotImplementedError

    def exists(self, _type, _id):
        """
        Check if a <type, id> pair exists
        :param _type:
        :param _id:
        :return:
        """
        raise NotImplementedError

    def clear(self):
        """
        Purge the database
        :return:
        """
        raise NotImplementedError

    def get_all(self, _type):
        """
        Get all values of `_type`
        :param _type:
        :return:
        """
        raise NotImplementedError

    def get_option(self, option_name):
        """
        Return an option
        :param option_name:
        :return:
        """
        raise NotImplementedError

    def set_option(self, option_name, value):
        """
        Set an option
        :param option_name:
        :param value:
        :return:
        """
        raise NotImplementedError


class MemoryBackend(Backend):
    """
    An in memory implementation of the backend.
    """
    _data = {'__option': {}}
    _id = {}

    def get(self, type_name, value_id):
        try:
            return self._data[type_name][value_id]
        except:
            raise IndexError

    def post(self, type_name, value_id, obj):
        if type_name not in self._data:
            self._data[type_name] = {}

        if not self.id_available(value_id):
            raise IndexError("Index already in use")

        self._data[type_name][value_id] = obj
        self._id[value_id] = True

    def put(self, type_name, value_id, obj):
        if self.exists(type_name, value_id):
            self._data[type_name][value_id] = obj
            return True
        return False

    def delete(self, obj):
        if obj:
            if self.exists(obj.type, obj.id):
                del self._data[obj.type][obj.id]
                return True
        return False

    def id_available(self, value_id):
        return value_id not in self._id

    def exists(self, type_name, value_id):
        if type_name in self._data:
            return value_id in self._data[type_name]
        return False

    def clear(self):
        self._data = {'__option': {}}
        self._id = {}

    def get_all(self, type_name):
        try:
            return self._data[type_name].values()
        except:
            raise KeyError

    def set_option(self, option_name, value):
        self._data['__option'][option_name] = value

    def get_option(self, option_name):
        try:
            return self._data['__option'][option_name]
        except:
            raise KeyError


class PersistentBackend(Database, Backend):
    """
    A SQlite backed implementation of the backend.
    Uses the dispersy Database class.
    """

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

    CREATE TABLE IF NOT EXISTS option(key TEXT PRIMARY KEY, value BLOB);
    INSERT INTO option(key, value) VALUES('database_version', '""" + str(LATEST_DB_VERSION) + u"""');
    """

    def __init__(self, working_directory, database_name=DATABASE_PATH):
        super(PersistentBackend, self).__init__(path.join(working_directory, database_name))
        self.open()

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

    def get(self, type_name, value_id):
        db_query = u"SELECT value FROM `market` WHERE type_name = ? AND id = ?"
        db_result = self.execute(db_query, (unicode(type_name), unicode(value_id))).fetchall()

        if len(db_result) != 1:
            raise IndexError

        return db_result[0][0]

    def get_all(self, type_name):
        db_query = u"SELECT value FROM `market` WHERE type_name = ?"
        db_result = self.execute(db_query, (unicode(type_name),)).fetchall()

        return [t[0] for t in db_result]

    def post(self, type_name, value_id, obj):
        if not self.id_available(value_id):
            raise IndexError("Index already in use")

        db_query = u"INSERT INTO `market` (id, type_name, value) VALUES (?, ?, ?)"
        self.execute(db_query, (unicode(value_id), unicode(type_name), unicode(obj)))
        self.commit()

    def put(self, type_name, value_id, obj):
        if self.exists(type_name, value_id):
            db_query = u"UPDATE `market` SET value = ? WHERE id = ? AND type_name = ?"
            self.execute(db_query, (unicode(obj), unicode(value_id), unicode(type_name)))
            self.commit()
            return True
        else:
            return False

    def delete(self, obj):
        db_query = u"DELETE FROM `market` WHERE id = ?"
        cur = self.execute(db_query, (unicode(obj.id),))
        self.commit()
        return cur.rowcount > 0

    def id_available(self, value_id):
        db_query = u"SELECT COUNT(*) FROM `market` WHERE id = ?"
        db_result = self.execute(db_query, (unicode(value_id),)).fetchall()
        return db_result[0][0] == 0

    def exists(self, type_name, value_id):
        db_query = u"SELECT COUNT(*) FROM `market` WHERE id = ? AND type_name = ?"
        db_result = self.execute(db_query, (unicode(value_id), unicode(type_name))).fetchall()
        return db_result[0][0] == 1

    def clear(self):
        self.execute(u"DELETE FROM market")
        self.execute(u"DELETE FROM option")

    def set_option(self, option_name, value):
        db_query = u"INSERT INTO `option` (key, value) VALUES (?, ?)"
        self.execute(db_query, (unicode(option_name), unicode(value),))
        self.commit()

    def get_option(self, option_name):
        db_query = u"SELECT value FROM `option` WHERE key = ?"
        db_result = self.execute(db_query, (unicode(option_name),)).fetchall()

        if len(db_result) != 1:
            raise IndexError

        return db_result[0][0]
