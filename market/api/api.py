import time

from market.api.crypto import generate_key
from market.database.database import Database
from market.models.user import User


class MarketAPI(object):
    def __init__(self, database):
        assert isinstance(database, Database)
        self._database = database
        self._user_key = None

    @property
    def db(self):
        return self._database

    @property
    def user_key(self):
        return self._user_key

    def create_user(self):
        """ save the user's public key in the database """
        new_keys = generate_key()
        user = User(new_keys[0], time.time())  # Save the public key bin (HEX) in the database along with the register time.

        if self.db.post(user.type, user):
            self._user_key = new_keys[0]
            return [self.user_key, new_keys]
        else:
            return None

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

    def browse_system(self):
        """ open a dialog window to browse the user's system (to upload their private key) """
        pass

    def remember_user(self):
        """ save the user's login credentials on their system """
        pass

    def generate_keys(self):
        """ generate a new key pair """
        pass

    def check_role(self):
        """ check which role the user has """
        pass

    def create_borrowers_profile(self):
        """ save the borrower's personal information """
        pass

    def load_borrowers_profile(self):
        """ display the borrower's personal information """
        pass

    def create_loan_request(self):
        """ create a new loan request """
        pass

    def load_borrowers_loans(self):
        """ display all of the borrower's current loans """
        pass

    def load_borrowers_offers(self):
        """ display all of the borrower's current offers """
        pass

    def accept_offer(self):
        """ accept an offer """
        pass

    def reject_offer(self):
        """ reject an offer """
        pass

    def load_all_loan_request(self, bank_id):
        """ load all pending loan requests for a specific bank """
        pass

    def load_single_loan_request(self, loan_request_id):
        """ load a specific loan request to """
        pass

    def accept_loan_request(self, loan_request_id):
        """ accept a pending loan request """
        pass

    def reject_loan_request(self, loan_request_id):
        """ reject a pending loan request """
        pass
