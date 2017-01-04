import random

from market.models.loans import Mortgage
from scenarios.fake_provider import FakePayload


class Tasks(object):

    choice = [True, False]

    def __init__(self, api):
        self.api = api

    def handle_incoming_loan_request(self, bank):
        loan_requests = self.api.load_all_loan_requests(bank)
        # loop through them and randomly accept or deny a few
        for list in loan_requests:
            loan_request = list[0]
            print "Accepting a mortgage from ", self.api._get_user(loan_request.user_key)
            self.api.accept_loan_request(bank, FakePayload.accept_loan_request(loan_request))

    def accept_mortgages(self, user):
        user.update(self.api.db)
        mortgages = self.api.load_borrowers_offers(user)
        accepted = False
        for mortgage in mortgages:
            if isinstance(mortgage, Mortgage):
                print "Agreeing with the mortgage offer from ", mortgage.bank, " signed?: ", mortgage.signature_valid(self.api)
                self.api.accept_mortgage_offer(user, FakePayload.accept_mortgage_offer(mortgage))
                accepted = True

        return accepted
