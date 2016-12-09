import uuid

from market.database.backends import Backend
from market.models import DatabaseModel


class Database(object):
    def get(self, type, id):
        raise NotImplementedError

    def post(self, type, obj):
        raise NotImplementedError

    def put(self, type, id, obj):
        raise NotImplementedError

    def delete(self, type, id):
        raise NotImplementedError

    def get_all(self, type):
        raise NotImplementedError


class MockDatabase(Database):
    def __init__(self, backend):
        assert isinstance(backend, Backend)

        self._backend = backend

    def get(self, type, id):
        try:
            return DatabaseModel.decode(self._backend.get(type, id))
        except IndexError:
            return None

    def post(self, type, obj):
        assert isinstance(obj, DatabaseModel)
        try:
            id = obj.generate_id()
            while not self.backend.id_available(id):
                id = obj.generate_id(force=True)

            obj.save(id)
            self.backend.post(type, id, obj.encode())
            return id
        except IndexError:
            return False

    def put(self, type, id, obj):
        assert isinstance(obj, DatabaseModel)

        assert obj.id
        assert id == obj.id

        try:
            return self.backend.put(type, id, obj.encode())
        except IndexError:
            return False

    def delete(self, obj):
        assert isinstance(obj, DatabaseModel)
        raise NotImplementedError

    def get_all(self, type):
        try:
            items = self.backend.get_all(type)
            if items:
                return [DatabaseModel.decode(t) for t in items]
        except KeyError:
            return None

    @property
    def backend(self):
        return self._backend