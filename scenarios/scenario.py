import random

import time
from faker import Faker

from market import Global
from market.api.api import MarketAPI, STATUS
from market.models.loans import Campaign, Mortgage, LoanRequest, Investment
from market.models.user import User
from scenarios.fake_provider import FakePayload

import random


class Scenario(object):
    def __init__(self, api):
        assert isinstance(api, MarketAPI)
        self.api = api

    def create_banks(self):
        for bank_name in Global.BANKS:
            user = User(public_key=Global.BANKS[bank_name], time_added=0)
            user.role_id = 3
            self.api.db.post(user.type, user)

    def make_borrower(self, user):
        self.api.create_profile(user, FakePayload.profile(1))

    def make_investor(self, user):
        self.api.create_profile(user, FakePayload.profile(2))

    def create_loan_request(self, user):
        assert user.role_id == 1    # borrower
        self.api.create_loan_request(user, FakePayload.create_loan_request())

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
        assert user.role_id == 1    # borrower

        investments = []

        # Find all pending investment offers from the user
        for investment_id in user.investment_ids:
            investment = self.api.db.get(Investment._type, investment_id)
            assert isinstance(investment, Investment)

            if investment.status == STATUS.PENDING:
                investments.append(investment)

        # Reject a random pending investment
        rand = random.randint(0, len(investments) - 1)
        self.api.reject_investment_offer(user, FakePayload.reject_investment_offer(investments[rand]))

    def load_profile(self, user):
        self.api.load_profile(user)

    def load_investments(self, user):
        assert user.role_id == 2    # investor
        self.api.load_investments(user)

    def load_open_market(self):
        self.api.load_open_market()

    def load_borrowers_loans(self, user):
        assert user.role_id == 1    # borrower
        self.api.load_borrowers_loans(user)

    def load_borrowers_offers(self, user):
        assert user.role_id == 1    # borrower
        self.api.load_borrowers_offers(user)

    def load_all_loan_requests(self, user):
        assert user.role_id == 3    # bank
        self.api.load_all_loan_requests(user)

    def load_single_loan_request(self):
        pending_loan_requests = []

        # Get a random pending loan request
        loan_requests = self.api.db.get_all(LoanRequest._type)
        for loan_request in loan_requests:
            for loan_status in loan_request.status:
                if loan_status == STATUS.PENDING:
                    pending_loan_requests.append(loan_request)

        pending_loan_requests = list(set(pending_loan_requests))    # remove duplicate entries
        rand = random.randint(0, len(pending_loan_requests) - 1)

        self.api.load_single_loan_request(pending_loan_requests[rand])

    def load_bids(self):
        # Get all running campaigns
        campaigns = self.api.db.get_all(Campaign._type)
        mortgages = []
        for campaign in campaigns:
            assert isinstance(campaign, Campaign)
            if not campaign.completed:
                mortgages.append(self.api.db.get(Mortgage._type, campaign.mortgage_id))

        # Get a random campaign to load bids for
        rand = random.randint(0, len(mortgages) - 1)

        self.api.load_bids(mortgages[rand])

    def load_mortages(self, user):
        assert user.role_id == 3    # bank
        self.api.load_mortgages(user)

