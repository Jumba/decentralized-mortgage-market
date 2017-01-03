from market.database.backends import Backend
from market.models import DatabaseModel


class Database(object):
    """
    Database interface.
    """
    def get(self, _type, _id):
        """
        Return a databasemodel if in the database.
        :param _type: The `DatabaseModel` type name.
        :param _id:  The `DatabaseModel` id.
        :return: The `DatabaseModel` object or None
        """
        raise NotImplementedError

    def post(self, _type, obj):
        """
        Save a `DatabaseModel` to the database

        :param _type: The `DatabaseModel` type
        :param obj: The `DatabaseModel` object
        :return: If it succeeds the id, or None.
        """
        raise NotImplementedError

    def put(self, _type, _id, obj):
        """
        Replace a DatabaseModel.
        :param _type: The `DatabaseModel` type name
        :param _id: The id of the model being replaced
        :param obj: The object replacing the model
        :return: True if succesfully replaced, None if the model wasn't found, and thus wasn't replaced.
        """
        raise NotImplementedError

    def delete(self, obj):
        """
        Delete the given object from the database
        :param obj: The `DatabaseModel` object.
        :return: True if deleted, False otherwise.
        """
        raise NotImplementedError

    def get_all(self, _type):
        """
        Return all objects of the given type.
        :param _type: The type name
        :return: The list of types.
        """
        raise NotImplementedError


class MockDatabase(Database):
    """
    Implementation of the database interface.

    Honestly the name is misleading since it was due to be a `mock` implementation of the mortgage market.
    """

    # TODO: Refactor name.

    def __init__(self, backend):
        assert isinstance(backend, Backend)

        self._backend = backend

    def get(self, _type, _id):
        try:
            return DatabaseModel.decode(self._backend.get(_type, _id))
        except IndexError:
            return None

    def post(self, _type, obj):
        assert isinstance(obj, DatabaseModel)
        try:
            _id = obj.generate_id()
            while not self.backend.id_available(_id):
                _id = obj.generate_id(force=True)

            obj.save(_id)
            self.backend.post(_type, _id, obj.encode())
            return _id
        except IndexError:
            return False

    def put(self, _type, _id, obj):
        assert isinstance(obj, DatabaseModel)

        assert obj.id
        assert _id == obj.id

        try:
            return self.backend.put(_type, _id, obj.encode())
        except IndexError:
            return False

    def delete(self, obj):
        assert isinstance(obj, DatabaseModel)
        return self.backend.delete(obj)

    def get_all(self, _type):
        try:
            items = self.backend.get_all(_type)
            if items:
                return [DatabaseModel.decode(t) for t in items]
        except KeyError:
            return None

    @property
    def backend(self):
        return self._backend
