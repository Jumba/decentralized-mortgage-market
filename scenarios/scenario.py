import random

from faker import Faker

from market.api.api import MarketAPI, STATUS
from market.models.loans import Campaign, Mortgage, LoanRequest, Investment
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
        self.api.load_investments(user)

    def load_open_market(self):
        self.api.load_open_market()

    def load_borrowers_loans(self, user):
        self.api.load_borrowers_loans(user)

    def load_borrowers_offers(self, user):
        self.api.load_borrowers_offers(user)

    def load_all_loan_requests(self, user):
        self.api.load_all_loan_requests(user)

    def load_single_loan_request(self):
        # Get a random loan request
        loan_requests = self.api.db.get_all(LoanRequest._type)
        rand = random.randint(0, len(loan_requests) - 1)

        self.api.load_single_loan_request(loan_requests[rand])

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

