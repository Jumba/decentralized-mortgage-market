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
