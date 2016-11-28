class Database(object):
    def get(self, type, id):
        return NotImplementedError

    def post(self, type, obj):
        return NotImplementedError

    def put(self, type, id, obj):
        return NotImplementedError

    def delete(self, id):
        return NotImplementedError
