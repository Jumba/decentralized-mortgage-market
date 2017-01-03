from PyQt5 import QtWidgets

from market.api.api import STATUS


class InvestorsPortfolioController:
    """
    Create a InvestorsPortfolioController object that performs tasks on the Investor's Portfolio section of the gui.
    Takes a MainWindowController object during construction.
    """
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.investments_table = self.mainwindow.ip_investments_table

    def setup_view(self):
        """
        Update the table of the view with up-to-date data.
        """
        # Clear table
        self.investments_table.setRowCount(0)

        # Getting the investments from the investor
        investments = self.mainwindow.api.load_investments(self.mainwindow.app.user)

        # If the list is empty, do nothing. Otherwise fill table
        if investments:
            # Fill the investments table
            for investment, house, campaign, profile in investments:
                # Property Address, Campaign Status, Investment Status, Amount Invested, Interest, Duration
                address = house.address + ' ' + house.house_number + ', ' + house.postal_code

                if campaign.completed:
                    campaign_status = 'Completed'
                else:
                    campaign_status = 'Running'

                if investment.status == STATUS.ACCEPTED:
                    investment_status = 'Accepted'
                else:
                    investment_status = 'Pending'

                row_count = self.investments_table.rowCount()
                self.investments_table.insertRow(row_count)
                self.investments_table.setItem(row_count, 0, QtWidgets.QTableWidgetItem(address))
                self.investments_table.setItem(row_count, 1, QtWidgets.QTableWidgetItem(campaign_status))
                self.investments_table.setItem(row_count, 2, QtWidgets.QTableWidgetItem(investment_status))
                self.investments_table.setItem(row_count, 3, QtWidgets.QTableWidgetItem(str(investment.amount)))
                self.investments_table.setItem(row_count, 4, QtWidgets.QTableWidgetItem(str(investment.interest_rate)))
                self.investments_table.setItem(row_count, 5, QtWidgets.QTableWidgetItem(str(investment.duration)))
