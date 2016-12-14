from market import Global
from market.api.api import MarketAPI
from market.database.backends import PersistentBackend, MemoryBackend
from market.database.database import MockDatabase
from marketGUI.market_app import MarketApplication, MarketApplicationABN
from scenarios.scenario import Scenario
from scenarios.tasks import Tasks


class MarketAppSceneBorrower(MarketApplication):

    bank_status = {}
    port = 1453
    database_prefix = 'borrower'

    def __init__(self, *argv):
        self.profile = False
        self.loan_request = False
        self.mortgage_accept = False
        self.investor_accept = False

        MarketApplication.__init__(self, *argv)

    def initialize_api(self):
        #self._api = MarketAPI(MockDatabase(PersistentBackend('.', u'sqlite/%s-market.db' % self.database_prefix)))
        self._api = MarketAPI(MockDatabase(MemoryBackend()))

    def _scenario(self):
        self.scenario = Scenario(self.api)

        if not self.profile and not self.loan_request and not self.mortgage_accept and not self.investor_accept:
            for bank_id in Global.BANKS:
                user = self.api._get_user(Global.BANKS[bank_id])
                if user.id in self.api.user_candidate:
                    print bank_id, " is ONLINE"
                    self.bank_status[bank_id] = True
                    self.profile = True
                else:
                    if not bank_id in self.bank_status:
                        self.bank_status[bank_id] = False
                        print bank_id, " is OFFLINE"


        if self.profile:
            print "Creating profile"
            # Creating a borrower
            self.scenario.make_borrower(self.user)
            self.profile = False
            self.loan_request = True

        # Creating a loan request
        if self.loan_request:
            print "Creating loan request"
            self.user.update(self.api.db)
            self.scenario.create_loan_request(self.user)
            self.loan_request = False
            self.mortgage_accept = False

        # Try an accept an offer
        if self.mortgage_accept:
            pass


class MarketAppSceneBank(MarketApplicationABN):
    def __init__(self, *argv):
        self.profile = True
        self.loan_request = False
        self.mortgage_accept = False
        self.investor_accept = False

        MarketApplicationABN.__init__(self, *argv)

    def _scenario(self):
        self.scenario = Scenario(self.api)
        self.tasks = Tasks(self.api)

        self.tasks.handle_incoming_loan_request(self.user)


