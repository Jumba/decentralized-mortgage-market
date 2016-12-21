from PyQt5 import uic
from PyQt5.QtWidgets import *

from market.controllers.banks_portfolio_controller import BanksPortfolioController
from market.controllers.campaign_bids_controller import CampaignBidsController
from market.controllers.investors_portfolio_controller import InvestorsPortfolioController
from market.controllers.pending_loan_requests_1_controller import PendingLoanRequests1Controller
from market.controllers.pending_loan_requests_2_controller import PendingLoanRequests2Controller
from navigation import NavigateUser
from login_controller import LoginController
from profile_controller import ProfileController
from borrowers_portfolio_controller import BorrowersPortfolioController
from openmarket_controller import OpenMarketController
from place_loan_request_controller import PlaceLoanRequestController


class MainWindowController(QMainWindow):
    def __init__(self, parent=None, app=None, ui_location='ui/mainwindow.ui'):
        super(MainWindowController, self).__init__(parent)
        self.app = app
        self.api = app.api
        uic.loadUi(ui_location, self)
        self.navigation = NavigateUser(self)
        self.fip_controller = BanksPortfolioController(self)
        self.bp_controller = BorrowersPortfolioController(self)
        self.cb_controller = CampaignBidsController(self)
        self.ip_controller = InvestorsPortfolioController(self)
        self.login_controller = LoginController(self)
        self.openmarket_controller = OpenMarketController(self)
        self.icb_controller = CampaignBidsController(self)
        self.fiplr1_controller = PendingLoanRequests1Controller(self)
        self.fiplr2_controller = PendingLoanRequests2Controller(self)
        self.bplr_controller = PlaceLoanRequestController(self)
        self.profile_controller = ProfileController(self)
        self.msg = QMessageBox

        self.setup_view()

    def setup_view(self):
        # If user is a bank, show the bank's portfolio. Otherwise show profile
        if self.app.user.role_id == 3:
            self.navigation.switch_to_banks_portfolio()
            self.navigation.set_bank_navigation()
        elif self.app.user.role_id == 2:
            self.navigation.switch_to_profile()
            self.navigation.set_investor_navigation()
        elif self.app.user.role_id == 1:
            self.navigation.switch_to_profile()
            self.navigation.set_borrower_navigation()
        else:
            self.navigation.switch_to_profile()

    # @staticmethod
    def insert_row(self, table, row):
        rowcount = table.rowCount()  # necessary even when there are no rows in the table
        table.insertRow(rowcount)
        for i in range(0, len(row)):
            table.setItem(rowcount, i, QTableWidgetItem(str(row[i])))

    def show_dialog(self, title, message):
        self.msg.about(self, title, message)
