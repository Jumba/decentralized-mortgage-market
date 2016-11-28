import hashlib
import time
import uuid

from market.database.backends import Backend
from market.database.database import Database


class MockDB(Database):
    def __init__(self, backend):
        assert isinstance(backend, Backend)

        self._backend = backend

    def get(self, type, id):
        try:
            return self._backend.get(type, id)
        except IndexError:
            return None

    def post(self, type, obj):
        try:
            id = uuid.uuid4()
            while not self.backend.id_available(id):
                id = uuid.uuid4()

            obj.save(id)
            self.backend.post(type, obj)
            return id
        except IndexError:
            return False

    def put(self, type, id, obj):
        assert obj.id
        assert id == obj.id

        try:
            return self.backend.put(type, id, obj)
        except IndexError:
            return False

    def delete(self, id):
        return NotImplementedError

    @property
    def backend(self):
        return self._backend