import time

from market.api.crypto import generate_key, get_public_key
from market.database.database import Database
from market.models.house import House
from market.models.loans import LoanRequest, Mortgage
from market.models.profiles import BorrowersProfile
from market.models.profiles import Profile
from market.models.role import Role
from market.models.user import User
from market.models.loans import Investment

STATUS = (
    'NONE',
    'PENDING',
    'ACCEPTED',
    'REJECTED'
)

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
        """
        Create a new user and saves it to the database.
        :return: A tuple (User, public_key, private_key) or None if saving failed.
        """
        new_keys = generate_key()
        user = User(public_key=new_keys[0], time_added=time.time())  # Save the public key bin (encode as HEX) in the database along with the register time.

        if self.db.post(user.type, user):
            return user, new_keys[0], new_keys[1]
        else:
            return None

    def login_user(self, private_key):
        """
        Login a user by generating the public key from the private key and grabbing the user object using the generated key.
        :param public_key:
        :param private_key:
        :return:
        """
        if get_public_key(private_key):
            user = self.db.get('users', get_public_key(private_key))

            return user
        return None

    def create_profile(self, user, payload):
        """
        Creates a new profile and saves it to the database.
        :param user:
        :param payload:
        :return:
        """
        assert isinstance(user, User)
        assert isinstance(payload, dict)

        try:
            role = Role(user.id, payload['role'])
            user.role_id = self.db.post(role.type, role)

            profile = None
            if role.role_name == 'INVESTOR':
                profile = Profile(payload['first_name'], payload['last_name'], payload['email'], payload['iban'], payload['phonenumber'])
            elif role.role_name == 'BORROWER':
                profile = BorrowersProfile(payload['first_name'], payload['last_name'], payload['email'], payload['iban'],
                                           payload['phonenumber'], payload['current_postalcode'], payload['current_housenumber'], payload['documents_list'])
            else:
                return False

            user.profile_id = self.db.post(profile.type, profile)
            self.db.put(user.type, user.id, user)
            return profile
        except KeyError:
            return False

    def load_profile(self, user):
        """
        Get the profile from the database.
        :param user:
        :return:
        """
        role = self.db.get('role', user.role_id)

        profile = None
        if role.role_name == 'INVESTOR':
            profile = self.db.get('profile', user.profile_id)
        elif role.role_name == 'BORROWER':
            profile = self.db.get('borrowers_profile', user.profile_id)
        else:
            return False

        return profile

    def place_loan_offer(self, user, payload):
        """
        Create a loan offer and save it to the database.
        :param user:
        :param payload:
        :return:
        """
        assert isinstance(user, User)
        assert isinstance(payload, dict)

        try:
            role = Role(user.id, payload['role'])
            user.role_id = self.db.post(role.type, role)

            loan_offer = None
            if role.role_name == 'INVESTOR':
                loan_offer = Investment(payload['user_key'], payload['amount'], payload['duration'], payload['interest_rate'],
                                        payload['mortgage_id'], payload['status'])
            else:
                return False

            user.investment_ids.append(self.db.post('investment', loan_offer))

            self.db.put(user.type, user.id, user)
            return loan_offer
        except KeyError as e:
            print "KeyError: " + str(e)
            return False

    def resell_investment(self):
        """ post the data needed to resell the investment """
        pass

    def load_investments(self, user):
        """
        Get the current investments list and the pending investments list from the database.
        :param user:
        :return:
        """
        current_investments = []
        pending_investments = []
        for investment_id in user.investment_ids:
            if self.db.get('investment', investment_id).status == "accepted":
                current_investments.append(self.db.get('investment', investment_id))
            elif self.db.get('investment', investment_id).status == "pending":
                pending_investments.append(self.db.get('investment', investment_id))
            else:
                pass
        return current_investments, pending_investments

    def load_open_market(self):
        """ get the 'to be displayed on the open market' data  """
        pass

    def check_role(self, user):
        """
        Get the role of the user from the database.
        :param user:
        :return:
        """
        return self.db.get('role', user.role_id)

    # TODO Add the created loan request to the bank's pending loan request list
    def create_loan_request(self, user, payload):
        """ Create a new loan request """
        assert isinstance(user, User)
        assert isinstance(payload, dict)

        role = self.db.get('role', user.role_id)

        loan_request = None
        if role.role_name == 'BORROWER':
            if user.loan_request_id is None:
                house = House(payload['postal_code'], payload['house_number'], payload['price'])
                house_id = str(self.db.post('house', house))
                payload['house_id'] = house_id
                payload['status'] = payload['status'].fromkeys(payload['banks'], STATUS[1])
                loan_request = LoanRequest(user.id, house_id, payload['mortgage_type'], payload['banks'], payload['description'], payload['amount_wanted'], payload['status'])
            else:
                return False
        else:
            return False

        user.loan_request_id = self.db.post('loan_request', loan_request)
        self.db.put('users', user.id, user)

        return loan_request

    # TODO: write test for this function after the accept_offer has been implemented
    def load_borrowers_loans(self, user):
        """
        Get the borrower's current active loans (funding goal has been reached) or the not yet active loans (funding goal has not been reached yet)
        :param user: User-object, in this case the user has the role of a borrower
        :return: list of the loans, containing either the current active loans or the not yet active loans
        """
        loans = []
        for mortgage_id in user.mortgage_ids:
            if self.db.get('mortgage', mortgage_id).status == "accepted":
                mortgage = self.db.get('mortgage', mortgage_id)
                # Add the accepted mortgage in the loans list
                loans.append(mortgage)
                campaign = self.db.get('campaign', user.campaign_id)
                for investor_id in mortgage.investors:
                    investor = self.db.get('users', investor_id)
                    for investment_id in investor.investment_ids:
                        investment = self.db.get('investment', investment_id)
                        # Add the loan to the loans list if the mortgage id's match and the funding goal has been reached
                        if investment.mortgage_id == mortgage_id and campaign.status == True:
                            loans.append(investment)
                        # Add the loan to the loans list if the mortgage id's match and the funding goal has not been reached
                        elif investment.mortgage_id == mortgage_id and campaign.status == False:
                            loans.append(investment)

        return loans

    def load_borrowers_offers(self, user):
        """
        Get all the borrower's offers(mortgage offers or loan offers) from the database.
        :param user:
        :return:
        """
        offers = []
        for mortgage_id in user.mortgage_ids:
            # If the mortgage is already accepted, we get the loan offers from the investors
            if self.db.get('mortgage', mortgage_id).status == "accepted":
                mortgage = self.db.get('mortgage', mortgage_id)
                for investor_id in mortgage.investors:
                    investor = self.db.get('users', investor_id)
                    for investment_id in investor.investment_ids:
                        if self.db.get('investment', investment_id).status == "pending":
                            investment_offer = self.db.get('investment', investment_id)
                            offers.append(investment_offer)

                return offers
            # If the mortgage has not yet been accepted, get the mortgage offers from the banks
            elif self.db.get('mortgage', mortgage_id).status == "pending":
                mortgage = self.db.get('mortgage', mortgage_id)
                offers.append(mortgage)

        return offers

    def accept_offer(self):
        """ accept an offer """
        pass

    def reject_offer(self):
        """ reject an offer """
        pass

    def load_all_loan_requests(self, user):
        """ load all pending loan requests for a specific bank """
        assert isinstance(user, User)

        role = self.db.get('role', user.role_id)
        assert isinstance(role, Role)

        if role.role_name == 'FINANCIAL_INSTITUTION':
            pending_loan_requests = []

            # Only show loan requests that are still pending
            for pending_loan_request_id in user.pending_loan_request_ids:
                if self.db.get('loan_request', pending_loan_request_id).status[user.id] == STATUS[1]:
                    pending_loan_requests.append(pending_loan_request_id)

            return pending_loan_requests
        else:
            return False

    def load_single_loan_request(self, payload):
        """ load a specific loan request """
        assert isinstance(payload, dict)

        loan_request = self.db.get('loan_request', payload['loan_request_id'])
        assert isinstance(loan_request, LoanRequest)

        return loan_request

    def accept_loan_request(self, user, payload):
        """ accept a pending loan request """
        # TODO Make this work
        assert isinstance(user, User)
        assert isinstance(payload, dict)

        # Create the accepted loan request
        payload['status'][user.id] = STATUS[2]

        accepted_loan_request = LoanRequest(payload['user_key'], payload['house_id'], payload['mortgage_type'],
                                            payload['banks'], payload['description'], payload['amount_wanted'],
                                            payload['status'])
        assert isinstance(accepted_loan_request, LoanRequest)

        mortgage = Mortgage(accepted_loan_request.id, payload['house_id'], user.id, payload['amount'], payload['mortgage_type'], payload['interest_rate'], payload['max_invest_rate'], payload['default_rate'], payload['duration'], payload['risk'], payload['investors'], STATUS[1])
        borrower = self.db.get('users', payload['user_key'])
        assert isinstance(borrower, User)
        loan_request_id = borrower.loan_request_id

        # Add mortgage to borrower
        mortgage_id = self.db.post('mortgage', mortgage)
        borrower.mortgage_ids.append(mortgage_id)
        self.db.put(borrower.type, borrower.id, borrower)

        # Save the accepted loan request
        if self.db.put('loan_request', loan_request_id, accepted_loan_request):
            return accepted_loan_request, mortgage
        else:
            return None

    def reject_loan_request(self, user, payload):
        """ reject a pending loan request """
        # TODO Make this work
        assert isinstance(user, User)
        assert isinstance(payload, dict)

        # Create the rejected loan request
        payload['status'][user.id] = STATUS[3]

        rejected_loan_request = LoanRequest(payload['user_key'], payload['house_id'], payload['mortgage_type'], payload['banks'], payload['description'], payload['amount_wanted'], payload['status'])
        assert isinstance(rejected_loan_request, LoanRequest)

        # Check if the loan request has been rejected by all selected banks
        rejected = True
        for bank in payload['status']:
            if payload['status'][bank] != STATUS[3]:
                rejected = False

        borrower = self.db.get('users', payload['user_key'])
        assert isinstance(borrower, User)
        loan_request_id = borrower.loan_request_id

        # If all banks have rejected the loan request, remove the loan request from borrower
        if rejected:
            borrower.loan_request_id = None
            self.db.put(borrower.type, borrower.id, borrower)

        # Save the rejected loan request
        if self.db.put('loan_request', loan_request_id, rejected_loan_request):
            return rejected_loan_request
        else:
            return None
