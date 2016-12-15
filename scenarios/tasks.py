import random

from scenarios.fake_provider import FakePayload


class Tasks(object):

    choice = [True, False]

    def __init__(self, api):
        self.api = api

    def handle_incoming_loan_request(self, bank):
        loan_requests = self.api.load_all_loan_requests(bank)

        # loop through them and randomly accept or deny a few
        for loan_request in loan_requests:
            print "Accepting a mortgage from ", self.api._get_user(loan_request.user_key)
            self.api.accept_loan_request(bank, FakePayload.accept_loan_request(loan_request))
