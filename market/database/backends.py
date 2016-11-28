class Backend(object):

    def get(self, type, id):
        return NotImplementedError

    def post(self, type, obj):
        return NotImplementedError

    def put(self, type, id, obj):
        return NotImplementedError

    def delete(self, id):
        return NotImplementedError

    def id_available(self, id):
        return NotImplementedError

    def exists(self, type, id):
       return NotImplementedError




class MemoryBackend(Backend):
    _data = {}
    _id = {}

    def get(self, type, id):
        try:
            return self._data[type][id]
        except:
            raise IndexError

    def post(self, type, obj):
        if type not in self._data:
            self._data[type] = {}

        if not self.id_available(obj.id):
            raise IndexError

        self._data[type][obj.id] = obj
        self._id[id] = True

    def put(self, type, id, obj):
        if self.exists(type, id):
            self._data[type][id] = obj
            return True
        return False

    def delete(self, id):
        return NotImplementedError

    def id_available(self, id):
        return id in self._id

    def exists(self, type, id):
        if type in self._data:
            return id in self._data[type]
        return False
