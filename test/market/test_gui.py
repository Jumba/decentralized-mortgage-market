from __future__ import absolute_import

import os
import sys
import unittest

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QStackedWidget, QDesktopWidget, QStackedLayout
from PyQt5.QtTest import QTest

from market.controllers.main_view_controller import MainWindowController
from market.views.main_view import Ui_MainWindow

from marketGUI.market_app import TestMarketApplication, MarketApplication


class GUITestSuite(unittest.TestCase):
    def setUp(self):
        self.app = TestMarketApplication(sys.argv)
        self.window = MainWindowController(app=self.app, ui_location=os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../', 'ui/mainwindow.ui'))
        user, _, _ = self.app.api.create_user()
        self.window.app.user = user
        # self.app.exec_()

    def tearDown(self):
        # sys.exit()
        pass
