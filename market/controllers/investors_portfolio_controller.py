import uuid
from PyQt5 import QtWidgets

from market.api.api import STATUS


class InvestorsPortfolioController:
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow

    def setup_view(self):
        # Clear table
        investments_table = self.mainwindow.ip_investments_table
        investments_table.clear()

        # Getting the investments from the investor
        investments = self.mainwindow.api.load_investments(self.mainwindow.app.user)

        # If the list is empty, do nothing. Otherwise fill table
        if investments:
            # Fill the investments table
            for [investment, house, campaign] in investments:
                # Property Address, Campaign Status, Investment Status, Amount Invested, Interest, Duration
                address = house.postal_code + ', ' + house.house_number

                campaign_status = ''
                if campaign.completed:
                    campaign_status = 'Completed'
                else:
                    campaign_status = 'Running'

                investment_status = ''
                if investment.status == STATUS.ACCEPTED:
                    investment_status = 'Accepted'
                else:
                    investment_status = 'Pending'

                row_count = investments_table.rowCount()
                investments_table.insertRow(row_count)
                investments_table.setItem(row_count, 0, QtWidgets.QTableWidgetItem(address))
                investments_table.setItem(row_count, 1, QtWidgets.QTableWidgetItem(campaign_status))
                investments_table.setItem(row_count, 2, QtWidgets.QTableWidgetItem(investment_status))
                investments_table.setItem(row_count, 3, QtWidgets.QTableWidgetItem(str(investment.amount)))
                investments_table.setItem(row_count, 4, QtWidgets.QTableWidgetItem(str(investment.interest_rate)))
                investments_table.setItem(row_count, 5, QtWidgets.QTableWidgetItem(str(investment.duration)))
