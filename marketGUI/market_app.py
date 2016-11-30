
from PyQt5.QtWidgets import QApplication


class MarketApplication(QApplication):
    """
    This class represents the main Tribler application.
    """
    def __init__(self, *argv):
        QApplication.__init__(self, *argv)


