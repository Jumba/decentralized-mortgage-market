import logging
import os


import time

import signal

logging.basicConfig(level=logging.WARNING, filename="market.log", filemode="a+",
                    format="%(asctime)-15s %(levelname)-8s %(message)s")

from PyQt5.QtWidgets import QApplication





class MarketApplication(QApplication):
    """
    This class represents the main Market application.
    """
    port = 1236
    database_prefix = 'market'

    def __init__(self, *argv):
        QApplication.__init__(self, *argv)


    def initialize(self):
        self.initialize_api()

        # Load banks
        from market import Global
        from market.models.user import User

        for bank_name in Global.BANKS:
            bank = self.api._get_user(Global.BANKS[bank_name]) or User(public_key=Global.BANKS[bank_name], time_added=0)
            bank.post_or_put(self.api.db)
            self.api.create_profile(bank, {'role': 3})
        #
        self.private_key = None
        self.user = None
        self.community = None

        self.identify()
        #
        signal.signal(signal.SIGINT, self.close)
        signal.signal(signal.SIGQUIT, self.close)

    def run(self):
        #print reactor
        # reactor.callWhenRunning(self.start_dispersy)
        # reactor.run()
        pass

    def close(self, *_):
        from twisted.internet import reactor
        self.dispersy.stop()
        reactor.stop()
        time.sleep(2)
        os._exit(1)

    def initialize_api(self):
        from market.api.api import MarketAPI
        from market.database.backends import PersistentBackend, MemoryBackend
        from market.database.database import MockDatabase
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
        from dispersy.dispersy import Dispersy
        from dispersy.endpoint import StandaloneEndpoint
        from market import Global
        from market.community.community import MortgageMarketCommunity
        from twisted.internet.task import LoopingCall

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


class MarketApplicationBank(MarketApplication):
    def initialize_api(self):
        from market.api.api import MarketAPI
        from market.database.database import MockDatabase
        from market.database.backends import PersistentBackend
        self._api = MarketAPI(MockDatabase(PersistentBackend('.', u'sqlite/%s-market.db' % self.database_prefix)))

    def identify(self):
        from market import Global
        self.private_key = Global.BANKS_PRIV[self.database_prefix]
        try:
            self.user = self.api.login_user(self.private_key.encode("HEX"))
            if not self.user:
                raise IndexError
        except IndexError:
            from market.models.user import User
            self.user = User(public_key=Global.BANKS[self.database_prefix], time_added=0)
            self.user.role_id = 3
            self.api.db.post(self.user.type, self.user)
            # login via the API to save/init database fields.

        if self.user and self.user.user_key == Global.BANKS[self.database_prefix]:
            print "Identified as ", self.database_prefix
            self.api.db.backend.set_option('user_key_pub', Global.BANKS[self.database_prefix])
            self.api.db.backend.set_option('user_key_priv', Global.BANKS_PRIV[self.database_prefix])
        else:
            print "failed to identify as ", self.database_prefix


class MarketApplicationABN(MarketApplicationBank):
    database_prefix = 'ABN'
    port = 1237


class MarketApplicationING(MarketApplicationBank):
    database_prefix = 'ING'
    port = 1239


class MarketApplicationRABO(MarketApplicationBank):
    database_prefix = 'RABO'
    port = 1240


class MarketApplicationMONEYOU(MarketApplicationBank):
    database_prefix = 'MONEYOU'
    port = 1241


class TestMarketApplication(QApplication):
    """
    This class represents the main Tribler application.
    """

    def __init__(self, *argv):
        QApplication.__init__(self, *argv)
        from market.api.api import MarketAPI
        from market.database.database import MockDatabase
        from market.database.backends import MemoryBackend
        from market.models.user import User
        from market.models.role import Role

        self._api = MarketAPI(MockDatabase(MemoryBackend()))
        # Create users
        user, _, _ = self._api.create_user()
        bank_role = Role.FINANCIAL_INSTITUTION.value
        bank1, _, _ = self._api.create_user()
        bank2, _, _ = self._api.create_user()
        bank3, _, _ = self._api.create_user()
        bank4, _, _ = self._api.create_user()
        bank1.role_id = bank_role
        bank2.role_id = bank_role
        bank3.role_id = bank_role
        bank4.role_id = bank_role
        self._api.db.put(User.type, bank1.id, bank1)
        self._api.db.put(User.type, bank2.id, bank2)
        self._api.db.put(User.type, bank3.id, bank3)
        self._api.db.put(User.type, bank4.id, bank4)
        self.user = user
        self.bank1 = bank1
        self.bank2 = bank2
        self.bank3 = bank3
        self.bank4 = bank4

    def run(self):
        self.exec_()

    @property
    def api(self):
        return self._api