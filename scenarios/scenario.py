from faker import Faker

from market.api.api import MarketAPI
from scenarios.fake_provider import FakePayload


class Scenario(object):
    def __init__(self, api):
        assert isinstance(api, MarketAPI)
        self.api = api

    def make_borrower(self, user):
        self.api.create_profile(user, FakePayload.profile(1))

    def make_investor(self, user):
        self.api.create_profile(user, FakePayload.profile(2))

    def create_loan_request(self, user):
        assert user.role_id == 1    # borrower
        self.api.create_loan_request(user, FakePayload.loan_request())

    def create_accepted_loan_request(self, user, loan_request):
        assert user.role_id == 3    # bank
        self.api.accept_loan_request(user, FakePayload.accept_loan_request(loan_request))

    def create_rejected_loan_request(self, user):
        pass

    def create_accepted_mortgage_offer(self, user):
        pass

    def create_rejected_mortgage_offer(self, user):
        pass

    def create_investment_offer(self, user):
        pass

    def create_accepted_investment_offer(self, user):
        pass

    def create_rejected_investment_offer(self, user):
        pass

    def load_profile(self, user):
        pass

    def load_investments(self, user):
        pass

    def load_open_market(self):
        pass

    def load_borrowers_loans(self, user):
        pass

    def load_borrowers_offers(self, user):
        pass

    def load_all_loan_requests(self, user):
        pass

    def load_single_loan_request(self):
        pass

    def load_bids(self):
        pass

