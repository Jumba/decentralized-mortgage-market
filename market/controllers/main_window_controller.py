from PyQt5 import uic

from PyQt5.QtWidgets import *
from market.controllers.banks_portfolio_controller import BanksPortfolioController
from market.controllers.campaign_bids_controller import CampaignBidsController
from market.controllers.investors_portfolio_controller import InvestorsPortfolioController
from market.controllers.pending_loan_requests_1_controller import PendingLoanRequests1Controller
from market.controllers.pending_loan_requests_2_controller import PendingLoanRequests2Controller
from navigation import NavigateUser
from profile_controller import ProfileController
from borrowers_portfolio_controller import BorrowersPortfolioController
from openmarket_controller import OpenMarketController
from place_loan_request_controller import PlaceLoanRequestController


class MainWindowController(QMainWindow):
    """

        Create a MainWindowController. Extends QMainWindow from the PyQt5 library.

        Takes a MarketApplication and the location of the ui file as parameters during construction.

        Used for hooking up the controllers to the view that is generated during runtime.

    """

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
        self.openmarket_controller = OpenMarketController(self)
        self.icb_controller = CampaignBidsController(self)
        self.fiplr1_controller = PendingLoanRequests1Controller(self)
        self.fiplr2_controller = PendingLoanRequests2Controller(self)
        self.bplr_controller = PlaceLoanRequestController(self)
        self.profile_controller = ProfileController(self)
        self.msg = QMessageBox
        self.setup_view()

    @staticmethod
    def filter_table(table, string, amount_column, amount_min, amount_max,  interest_column, interest_min, interest_max,
                     duration_column, duration_min, duration_max):
        """
            Passes all inputs to filter the given table with the filter_matching and filter_in_range methods.
        """
        MainWindowController.show_hidden(table)
        MainWindowController.filter_matching(table, string)
        MainWindowController.filter_in_range(table, amount_column, amount_min, amount_max)
        MainWindowController.filter_in_range(table, interest_column, interest_min, interest_max)
        MainWindowController.filter_in_range(table, duration_column, duration_min, duration_max)

    @staticmethod
    def filter_matching(table, string):
        """
            Hides all rows that don't contain the given substring.
        :param table: The given table that will be filtered.
        :param string: The substring that will be used to match the items in the table.
        """
        for i in range(0, table.rowCount()):
            matched = False
            for j in range(0, table.columnCount()):
                if string in str(table.item(i, j).text()):
                    matched = True
                    break
            if matched is False:
                table.hideRow(i)

    @staticmethod
    def filter_in_range(table, column, lower_bound, upper_bound):
        """
            Hides all rows which do not fit within a domain for a specific column.
        :param table: The given table that will be filtered.
        :param column: The column which will be checked.
        :param lower_bound: Lower bound of the domain.
        :param upper_bound: Upper bound of the domain.
        """
        if lower_bound and upper_bound:
            try:
                for i in range(0, table.rowCount()):
                    if not float(lower_bound) <= float(table.item(i, column).text()) <= float(upper_bound):
                        table.hideRow(i)
            except ValueError as e:
                print('Given input for lower or upper bound cannot be used.')
                print(e.message)

    @staticmethod
    def show_hidden(table):
        """
            Shows all rows of the given table.
        """
        for i in range(0, table.rowCount()):
            table.showRow(i)

    def closeEvent(self, event):
        self.app.close()

    def setup_view(self):
        """
            Calls the right user's navigation bar and redirects to the user's starting page.

        """
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

    @staticmethod
    def insert_row(table, row):
        """

            General method used by the controllers to insert rows with data into tables.

            :param table: QTableWidget object used for insertion
            :param row: A list of items that need to be inserted into the given table

        """
        rowcount = table.rowCount()  # necessary even when there are no rows in the table
        table.insertRow(rowcount)
        for i in range(0, len(row)):
            table.setItem(rowcount, i, QTableWidgetItem(str(row[i])))

    def show_dialog(self, title, message):
        """

            Shows a QMessageBox alert with the given title and message.

            The window has only an 'ok'-button
            The pop-up closes when this button is pressed.

            :param title: Title of the window as string
            :param message: Message that will be displayed inside the alert.

        """
        self.msg.about(self, title, message)

