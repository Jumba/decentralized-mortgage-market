import sys
import unittest
from PyQt5.QtWidgets import QMainWindow, QApplication, QStackedWidget, QDesktopWidget, QStackedLayout
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest

from marketGUI.market_app import MarketApplication
from marketGUI.market_window import MarketWindow


class GUITestSuite(unittest.TestCase):
    def setUp(self):
        self.MarketApplication = MarketApplication()
        self.MarketWindow = MarketWindow()

    def tearDown(self):
        self.MarketApplication.closeAllWindows()
        self.MarketWindow.close_market()
        self.MarketWindow.close()