from PyQt5 import QtWidgets

from market.api.api import STATUS


class InvestorsPortfolioController:
    """
    Create a InvestorsPortfolioController object that performs tasks on the Investor's Portfolio section of the gui.
    Takes a MainWindowController object during construction.
    """
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.table = self.mainwindow.ip_investments_table
        self.mainwindow.ip_search_lineedit.textChanged.connect(self.set_filters)
        self.mainwindow.ip_min_amount_lineedit.textChanged.connect(self.set_filters)
        self.mainwindow.ip_max_amount_lineedit.textChanged.connect(self.set_filters)
        self.mainwindow.ip_interest1_lineedit.textChanged.connect(self.set_filters)
        self.mainwindow.ip_interest2_lineedit.textChanged.connect(self.set_filters)
        self.mainwindow.ip_duration1_lineedit.textChanged.connect(self.set_filters)
        self.mainwindow.ip_duration2_lineedit.textChanged.connect(self.set_filters)

    def setup_view(self):
        """
        Sets up the view.
        """
        # Clear table
        self.table.setRowCount(0)

        # Getting the investments from the investor
        investments = self.mainwindow.api.load_investments(self.mainwindow.app.user)

        # If the list is empty, do nothing. Otherwise fill table
        if investments:
            # Fill the investments table
            self.fill_table(investments)

    def fill_table(self, investments):
        """
        Fills the table with investments.
        """
        for investment, house, campaign, profile in investments:
            # Property Address, Campaign Status, Investment Status, Amount Invested, Interest, Duration
            address = house.address + ' ' + house.house_number + ', ' + house.postal_code
            name = ' '
            iban = ' '

            if campaign.completed:
                campaign_status = 'Completed'
            else:
                campaign_status = 'Running'

            if investment.status == STATUS.ACCEPTED:
                investment_status = 'Accepted'
                name = profile.first_name + ' ' + profile.last_name
                iban = profile.iban
            else:
                investment_status = 'Pending'

            row_count = self.table.rowCount()
            self.table.insertRow(row_count)
            self.table.setItem(row_count, 0, QtWidgets.QTableWidgetItem(address))
            self.table.setItem(row_count, 1, QtWidgets.QTableWidgetItem(campaign_status))
            self.table.setItem(row_count, 2, QtWidgets.QTableWidgetItem(investment_status))
            self.table.setItem(row_count, 3, QtWidgets.QTableWidgetItem(str(investment.amount)))
            self.table.setItem(row_count, 4, QtWidgets.QTableWidgetItem(str(investment.interest_rate)))
            self.table.setItem(row_count, 5, QtWidgets.QTableWidgetItem(str(investment.duration)))
            self.table.setItem(row_count, 6, QtWidgets.QTableWidgetItem(name))
            self.table.setItem(row_count, 7, QtWidgets.QTableWidgetItem(iban))

    def set_filters(self):
        """
        Sets the method that gets called every time there is a change to the fields.
        """
        self.mainwindow.filter_table(self.table,
                                     self.mainwindow.ip_search_lineedit.text(),
                                     3,
                                     self.mainwindow.ip_min_amount_lineedit.text(),
                                     self.mainwindow.ip_max_amount_lineedit.text(),
                                     4,
                                     self.mainwindow.ip_interest1_lineedit.text(),
                                     self.mainwindow.ip_interest2_lineedit.text(),
                                     5,
                                     self.mainwindow.ip_duration1_lineedit.text(),
                                     self.mainwindow.ip_duration2_lineedit.text())
