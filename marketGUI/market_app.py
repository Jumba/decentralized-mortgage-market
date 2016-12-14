import logging

import time

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
    """
    This class represents the main Market application.
    """
    def __init__(self, *argv):
        QApplication.__init__(self, *argv)
        self.initialize_api()
        self.private_key = None
        self.user = None
        self.community = None

        self.identify()

        # Ready to start dispersy
        reactor.callWhenRunning(self.start_dispersy)
        reactor.run()

    def initialize_api(self):
        self._api = MarketAPI(MockDatabase(PersistentBackend('.')))


    def identify(self):
        """
        Identify the user to the system.

        If it already exists in the screen go on, if not create a user.
        """
        try:
            self.private_key = self.api.db.backend.get_option('user_key_priv')
            self.user = self.api.login_user(self.private_key.encode("HEX"))
            print "Using an existing user"
        except IndexError:
            user, _, priv = self.api.create_user()
            self.user = user
            self.private_key = priv
            print "Using a new user"



    def start_dispersy(self):
        dispersy = Dispersy(StandaloneEndpoint(1236, '0.0.0.0'), unicode('.'), u'dispersy.db')
        dispersy.statistics.enable_debug_statistics(True)
        dispersy.start(autoload_discovery=True)

        my_member = dispersy.get_member(private_key=self.private_key.decode("HEX"))
        master_member = dispersy.get_member(public_key=Global.MASTER_KEY)
        self.community = MortgageMarketCommunity.init_community(dispersy, master_member, my_member)
        self.community.api = self.api
        self.api.community = self.community



    @property
    def api(self):
        return self._api



class MarketApplicationABN(MarketApplication):

    bank_name = 'ABN'

    def initialize_api(self):
        self._api = MarketAPI(MockDatabase(PersistentBackend('.', u'%s-market.db' % self.bank_name)))


    def identify(self):
        self.private_key = Global.BANKS_PRIV[self.bank_name]
        try:
            print "Attempting login"
            self.user = self.api.login_user(self.private_key.encode("HEX"))
            if not self.user:
                raise IndexError
        except IndexError:
            print "Creating new user"
            self.user = User(public_key=Global.BANKS[self.bank_name], time_added=time.time())
            print self.user, " has been created."
            self.api.db.post(self.user.type, self.user)

        if self.user and self.user.user_key == Global.BANKS[self.bank_name]:
            print "Identified as ", self.bank_name, self.user.user_key
        else:
            print "failed to identify as ", self.bank_name
            print "User is ", self.user