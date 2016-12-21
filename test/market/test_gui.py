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
        self.app = TestMarketApplication(sys.argv)
        self.window = MainWindowController(app=self.app, ui_location=os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../', 'ui/mainwindow.ui'))
        self.window.bplr_controller.banks_ids = [self.window.app.bank1.id, self.window.app.bank2.id,
                                                 self.window.app.bank3.id, self.window.app.bank4.id]

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

    def test_investors_portfolio_table_empty(self):
        pass

    def test_investors_portfolio_table_filled(self):
        # TODO Add accepted and pending investments with running and completed campaigns
        pass

    def test_banks_portfolio_table_empty(self):
        pass

    def test_banks_portfolio_table_filled(self):
        # TODO Add running and completed campaigns
        pass

    def test_pending_loan_requests_table_empty(self):
        pass

    def test_pending_loan_requests_table_filled(self):
        # TODO Add loan requests for linear and fixed-rate mortgages
        pass

    def test_pending_loan_requests_table_unselected(self):
        pass

    def test_pending_loan_requests_table_selected(self):
        pass

    def test_pending_loan_request_forms_filled(self):
        # TODO Test for linear and fixed-rate mortgages
        pass

    def test_pending_loan_request_accept_empty(self):
        pass

    def test_pending_loan_request_accept_filled_incomplete(self):
        pass

    def test_pending_loan_request_accept_filled_complete(self):
        pass

    def test_pending_loan_request_reject_empty(self):
        pass

    def test_pending_loan_request_reject_filled(self):
        pass
