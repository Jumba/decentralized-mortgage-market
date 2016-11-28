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

    def login_user(self):
        """ get the user_key """
        pass

    def modify_profile(self):
        """ post the data in profile """
        pass

    def place_loan_offer(self):
        """ post the data needed for placing a loan offer """
        pass

    def resell_investment(self):
        """ post the data needed to resell the investment """
        pass

    def load_investments(self):
        """ get the data from current and pending investments """
        pass

    def load_open_market(self):
        """ get the 'to be displayed on the open market' data  """
        pass