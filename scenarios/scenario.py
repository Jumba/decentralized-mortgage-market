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
        assert user.role_id == 1
        self.api.create_loan_request(user, FakePayload.loan_request())
