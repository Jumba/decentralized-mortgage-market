from faker import Faker

from market.api.api import MarketAPI
from scenarios.fake_provider import FakePayload

import random


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

    def create_accepted_loan_request(self, user):
        assert user.role_id == 3

        while x == True:
            loan_request = self.db.get('loan_request', random.randint(0, len(user.loan_request_ids)-1))
            if loan_request.status == self.api.STATUS.PENDING:
                x = False
                self.api.accept_loan_request(user, FakePayload.accept_loan_request(loan_request))

    def create_rejected_loan_request(self, user):
        assert user.role_id == 3

        while x == True:
            loan_request = self.db.get('loan_request', random.randint(0, len(user.loan_request_ids)-1))
            if loan_request.status == self.api.STATUS.PENDING:
                x = False
                self.api.reject_loan_request(user, FakePayload.reject_loan_request(loan_request))


    def create_accepted_mortgage_offer(self, user):
        assert user.role_id == 1

        while x == True:
            mortgage = self.db.get('mortgage', random.randint(0, len(user.mortgage_ids)-1))
            if mortgage.status == self.api.STATUS.PENDING:
                x = False
                self.api.accept_mortgage_offer(user, FakePayload.accept_mortgage_offer(mortgage))

    def create_rejected_mortgage_offer(self, user):
        assert user.role_id == 1

        while x == True:
            mortgage = self.db.get('mortgage', random.randint(0, len(user.mortgage_ids)-1))
            if mortgage.status == self.api.STATUS.PENDING:
                x = False
                self.api.reject_mortgage_offer(user, FakePayload.reject_mortgage_offer(mortgage))

    def create_investment_offer(self, user):
        assert user.role_id == 2

        while x == True:
            mortgage = random.choice(self.api.db.get_all('mortgage'))
            if mortgage.status == self.api.STATUS.ACCEPTED:
                x = False
                self.api.place_loan_offer(user, FakePayload.place_investment_offer(mortgage))

    def create_accepted_investment_offer(self, user):
        assert user.role_id == 1

        while x == True:
            investment = self.db.get('investment', random.randint(0, len(user.investment_ids)-1))
            if investment.status == self.api.STATUS.ACCEPTED:
                x = False
                self.api.accept_investment_offer(user, FakePayload.accept_investment_offer(investment))

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

    def load_mortages(self):
        pass

