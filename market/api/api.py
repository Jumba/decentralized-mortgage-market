class MarketAPI(object):

    def get(self, id):
        pass

    def put(self, id, payload):
        pass

    def post(self, payload):
        if payload(type) == 'house':
            # use the house handler
            pass
        elif payload(type) == 'loan':
            # ditto
            pass

    def delete(self, id):
        pass

    def create_user(self):
        # bla bla
        self.post('user', ('example', 'example2'))