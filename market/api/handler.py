class Handler(object):
    def get(self, id):
        return NotImplementedError

    def put(self, id, payload):
        return NotImplementedError

    def post(self, payload):
        return NotImplementedError

    def delete(self, id):
        return NotImplementedError