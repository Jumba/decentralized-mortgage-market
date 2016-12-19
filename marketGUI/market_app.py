import logging

from market.models.user import User

logging.basicConfig(level=logging.WARNING, filename="market.log", filemode="a+",
                    format="%(asctime)-15s %(levelname)-8s %(message)s")

from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from PyQt5.QtWidgets import QApplication

from market import Global
from market.api.api import MarketAPI
from market.community.community import MortgageMarketCommunity
from market.database.backends import PersistentBackend
from market.database.database import MockDatabase
from market.dispersy.dispersy import Dispersy
from market.dispersy.endpoint import StandaloneEndpoint


class MarketApplication(QApplication):
    port = 1236
    database_prefix = ''

    """
    This class represents the main Market application.
    """

    def __init__(self, *argv):
        QApplication.__init__(self, *argv)
        self.initialize_api()

        # Load banks
        for bank_name in Global.BANKS:
            bank = self.api._get_user(Global.BANKS[bank_name]) or User(public_key=Global.BANKS[bank_name], time_added=0)
            bank.post_or_put(self.api.db)
            self.api.create_profile(bank, {'role': 3})


        self.private_key = None
        self.user = None
        self.community = None

        self.identify()

        # Ready to start dispersy
        reactor.callWhenRunning(self.start_dispersy)
        reactor.run()

    def initialize_api(self):
        self._api = MarketAPI(MockDatabase(PersistentBackend('.', u'sqlite/market.db')))

    def identify(self):
        """
        Identify the user to the system.

        If it already exists in the screen go on, if not create a user.
        """
        try:
            self.private_key = self.api.db.backend.get_option('user_key_priv')
            self.user = self.api.login_user(self.private_key.encode("HEX"))
            print "Using an existing user"
        except (KeyError, IndexError):
            user, _, priv = self.api.create_user()
            self.user = user
            self.private_key = priv
            print "Using a new user"

    def start_dispersy(self):
        self.dispersy = Dispersy(StandaloneEndpoint(self.port, '0.0.0.0'), unicode('.'), u'dispersy-%s.db' % self.database_prefix)
        self.dispersy.statistics.enable_debug_statistics(True)
        self.dispersy.start(autoload_discovery=True)

        my_member = self.dispersy.get_member(private_key=self.private_key.decode("HEX"))
        master_member = self.dispersy.get_member(public_key=Global.MASTER_KEY)
        self.community = MortgageMarketCommunity.init_community(self.dispersy, master_member, my_member)
        self.community.api = self.api
        self.community.user = self.user
        self.api.community = self.community

        # Run the scenario every 3 seconds
        LoopingCall(self._scenario).start(3.0)

        # Send messages from the queue every 3 seconds
        LoopingCall(self.api.outgoing_queue.process).start(3.0)
        LoopingCall(self.api.incoming_queue.process).start(3.0)

    def _scenario(self):
        pass

    @property
    def api(self):
        return self._api


class MarketApplicationABN(MarketApplication):
    database_prefix = 'ABN'
    port = 1237

    def initialize_api(self):
        self._api = MarketAPI(MockDatabase(PersistentBackend('.', u'sqlite/%s-market.db' % self.database_prefix)))

    def identify(self):
        self.private_key = Global.BANKS_PRIV[self.database_prefix]
        try:
            print "Attempting login"
            self.user = self.api.login_user(self.private_key.encode("HEX"))
            if not self.user:
                raise IndexError
        except IndexError:
            print "Creating new user"
            self.user = User(public_key=Global.BANKS[self.database_prefix], time_added=0)
            self.user.role_id = 3
            print self.user, " has been created."
            self.api.db.post(self.user.type, self.user)
            # login via the API to save/init database fields.

        if self.user and self.user.user_key == Global.BANKS[self.database_prefix]:
            print "Identified as ", self.database_prefix
            self.api.db.backend.set_option('user_key_pub', Global.BANKS[self.database_prefix])
            self.api.db.backend.set_option('user_key_priv', Global.BANKS_PRIV[self.database_prefix])
        else:
            print "failed to identify as ", self.database_prefix
            print "User is ", self.user


class MarketApplicationING(MarketApplication):
    database_prefix = 'ING'
    port = 1239

    def initialize_api(self):
        self._api = MarketAPI(MockDatabase(PersistentBackend('.', u'sqlite/%s-market.db' % self.database_prefix)))

    def identify(self):
        self.private_key = Global.BANKS_PRIV[self.database_prefix]
        try:
            print "Attempting login"
            self.user = self.api.login_user(self.private_key.encode("HEX"))
            if not self.user:
                raise IndexError
        except IndexError:
            print "Creating new user"
            self.user = User(public_key=Global.BANKS[self.database_prefix], time_added=0)
            self.user.role_id = 3
            print self.user, " has been created."
            self.api.db.post(self.user.type, self.user)

        if self.user and self.user.user_key == Global.BANKS[self.database_prefix]:
            print "Identified as ", self.database_prefix
        else:
            print "failed to identify as ", self.database_prefix
            print "User is ", self.user
