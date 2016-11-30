
from PyQt5.QtWidgets import QApplication

from market.api.api import MarketAPI
from market.database.backends import PersistentBackend
from market.database.database import MockDatabase


class MarketApplication(QApplication):
    """
    This class represents the main Tribler application.
    """
    def __init__(self, *argv):
        QApplication.__init__(self, *argv)
        self._api = MarketAPI(MockDatabase(PersistentBackend('.')))

    @property
    def api(self):
        return self._api

