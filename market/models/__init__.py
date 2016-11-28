class DatabaseModel(object):
    def save(self, id):
        self._id = id

    @property
    def id(self):
        return self._id
