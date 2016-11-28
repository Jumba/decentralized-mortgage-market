class Handler(object):
    def get(self, hash):
        return NotImplementedError

    def put(self, hash, payload):
        return NotImplementedError

    def post(self, payload):
        return NotImplementedError

    def delete(self, hash):
        return NotImplementedError