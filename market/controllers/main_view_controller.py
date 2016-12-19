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
    def __init__(self, parent=None, app=None):
        super(MainWindowController, self).__init__(parent)
        self.app = app
        self.api = app.api
        uic.loadUi('ui/mainwindow.ui', self)
        self.navigation = NavigateUser(self)
        self.bank_ids = []  # List with the hardcoded bank ids
        self.stackedWidget.setCurrentIndex(0)
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

    # @staticmethod
    def insert_row(self, table, row):
        rowcount = table.rowCount()  # necessary even when there are no rows in the table
        table.insertRow(rowcount)
        for i in range(0, len(row)):
            table.setItem(rowcount, i, QTableWidgetItem(str(row[i])))

