from marketGUI.market_app import MarketApplication, MarketApplicationABN
from scenarios.scenario import Scenario
from scenarios.tasks import Tasks


class MarketAppSceneBorrower(MarketApplication):
    def __init__(self, *argv):
        profile = True
        loan_request = False
        mortgage_accept = False
        investor_accept = False

        MarketApplication.__init__(self, *argv)

    def _scenario(self):
        self.scenario = Scenario(self.api)

        if self.profile:
            # Creating a borrower
            self.scenario.make_borrower(self.user)
            self.profile = False
            self.loan_request = True

        # Creating a loan request
        if self.loan_request:
            self.scenario.create_loan_request(self.user)
            self.loan_request = False
            self.mortgage_accept = True

        # Try an accept an offer
        if self.mortgage_accept:
            pass


class MarketAppSceneBank(MarketApplicationABN):
    def __init__(self, *argv):
        profile = True
        loan_request = False
        mortgage_accept = False
        investor_accept = False

        MarketApplicationABN.__init__(self, *argv)

    def _scenario(self):
        self.scenario = Scenario(self.api)
        self.tasks = Tasks(self.api)

        self.tasks.handle_incoming_loan_request(self.user)


