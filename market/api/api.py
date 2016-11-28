class MarketAPI(object):

    def get(self, type, id):
        pass

    def put(self, type, id, payload):
        pass

    def post(self, type, payload):
        if type == 'house':
            # use the house handler
            pass
        elif type == 'loan':
            # ditto
            pass

    def delete(self, id):
        pass

    def create_user(self):
        # bla bla
        self.post('user', ('example', 'example2'))