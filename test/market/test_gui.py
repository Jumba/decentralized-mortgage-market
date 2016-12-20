from __future__ import absolute_import

import os
import sys
import unittest

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QStackedWidget, QDesktopWidget, QStackedLayout
from PyQt5.QtTest import QTest

from market.controllers.main_view_controller import MainWindowController
from market.controllers.profile_controller import ProfileController
from market.models.user import User
from market.views.main_view import Ui_MainWindow

from marketGUI.market_app import TestMarketApplication, MarketApplication

from mock import Mock, MagicMock


class GUITestSuite(unittest.TestCase):
    def setUp(self):
        # self.app = Mock(spec=TestMarketApplication)
        # self.window = Mock(spec=MainWindowController())
        self.app = TestMarketApplication(sys.argv)
        self.window = MainWindowController(app=self.app, ui_location=os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../', 'ui/mainwindow.ui'))
        user, _, _ = self.app.api.create_user()
        self.window.app.user = Mock(User)
        # self.app.exec_()

    def tearDown(self):
        # sys.exit()
        pass

    def test_profile_empty(self):
        self.window.profile_controller.msg.about = MagicMock()
        QTest.mouseClick(self.window.profile_save_pushbutton, Qt.LeftButton)
        self.window.profile_controller.msg.about.assert_called_with(self.window, 'Profile error', 'You didn\'t enter all of the required information.')

    def test_profile_switch_role(self):
        pass

