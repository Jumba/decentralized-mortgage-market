from PyQt5 import QtWidgets


class BanksPortfolioController:
    """
    Create a BanksPortfolioController object that performs tasks on the Bank's Portfolio section of the gui.
    Takes a MainWindowController object during construction.
    """
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.table = self.mainwindow.fip_campaigns_table

        self.mainwindow.fip_search_lineedit.textChanged.connect(self.set_filters)
        self.mainwindow.fip_min_amount_lineedit.textChanged.connect(self.set_filters)
        self.mainwindow.fip_max_amount_lineedit.textChanged.connect(self.set_filters)
        self.mainwindow.fip_interest1_lineedit.textChanged.connect(self.set_filters)
        self.mainwindow.fip_interest2_lineedit.textChanged.connect(self.set_filters)
        self.mainwindow.fip_duration1_lineedit.textChanged.connect(self.set_filters)
        self.mainwindow.fip_duration2_lineedit.textChanged.connect(self.set_filters)

    def setup_view(self):
        """
        Update the table of the view with up-to-date data.
        """
        # Clear table
        self.table.setRowCount(0)

        # Getting the mortgages from the bank
        mortgages = self.mainwindow.api.load_mortgages(self.mainwindow.app.user)

        # If the list is empty, do nothing. Otherwise fill table
        if mortgages:
            # Fill the mortgage table
            for [mortgage, house, campaign, profile] in mortgages:
                # Property Address, Campaign Status, Investment Status, Amount Invested, Interest, Duration
                address = house.address + ' ' + house.house_number + ', ' + house.postal_code

                if campaign.completed:
                    campaign_status = 'Completed'
                else:
                    campaign_status = 'Running'

                row_count = self.table.rowCount()
                self.table.insertRow(row_count)
                self.table.setItem(row_count, 0, QtWidgets.QTableWidgetItem(address))
                self.table.setItem(row_count, 1, QtWidgets.QTableWidgetItem(campaign_status))
                self.table.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str(mortgage.amount)))
                self.table.setItem(row_count, 3, QtWidgets.QTableWidgetItem(str(mortgage.interest_rate)))
                self.table.setItem(row_count, 4, QtWidgets.QTableWidgetItem(str(mortgage.default_rate)))
                self.table.setItem(row_count, 5, QtWidgets.QTableWidgetItem(str(mortgage.duration)))
                self.table.setItem(row_count, 6, QtWidgets.QTableWidgetItem(profile.first_name + ' ' +
                                                                            profile.last_name))
                self.table.setItem(row_count, 7, QtWidgets.QTableWidgetItem(profile.iban))

    def set_filters(self):
        self.mainwindow.filter_table(self.table,
                                     self.mainwindow.fip_search_lineedit.text(),
                                     2,
                                     self.mainwindow.fip_min_amount_lineedit.text(),
                                     self.mainwindow.fip_max_amount_lineedit.text(),
                                     3,
                                     self.mainwindow.fip_interest1_lineedit.text(),
                                     self.mainwindow.fip_interest2_lineedit.text(),
                                     5,
                                     self.mainwindow.fip_duration1_lineedit.text(),
                                     self.mainwindow.fip_duration2_lineedit.text())
