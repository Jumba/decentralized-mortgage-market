from datetime import datetime

from PyQt5.QtWidgets import *


class OpenMarketController:
    """
    Create a ProfileController object that performs tasks on the Profile section of the gui.
    Takes a MainWindowController object during construction.
    """
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.content = None
        self.table = self.mainwindow.openmarket_open_market_table
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.doubleClicked.connect(self.view_campaign)
        self.mainwindow.openmarket_view_loan_bids_pushbutton.clicked.connect(self.view_campaign)

        self.mainwindow.openmarket_search_lineedit.textChanged.connect(self.set_filters)
        self.mainwindow.openmarket_max_amount_lineedit.textChanged.connect(self.set_filters)
        self.mainwindow.openmarket_min_amount_lineedit.textChanged.connect(self.set_filters)
        self.mainwindow.openmarket_interest1_lineedit.textChanged.connect(self.set_filters)
        self.mainwindow.openmarket_interest2_lineedit.textChanged.connect(self.set_filters)
        self.mainwindow.openmarket_duration1_lineedit.textChanged.connect(self.set_filters)
        self.mainwindow.openmarket_duration2_lineedit.textChanged.connect(self.set_filters)

    def setup_view(self):
        """
        Setup the open market table with up-to-date data.
        """
        self.table.setRowCount(0)
        self.content = self.mainwindow.api.load_open_market()
        for tpl in self.content:
            mortgage = tpl[0]
            campaign = tpl[1]
            house = tpl[2]
            row = [house.address + ' ' + house.house_number + ', ' + house.postal_code, campaign.amount,
                   mortgage.interest_rate, mortgage.duration, (campaign.end_date - datetime.now()).days, mortgage.risk]
            self.mainwindow.insert_row(self.table, row)

    def view_campaign(self):
        """
        View a selected campaign. Redirects to the a "Campaign Bids" screen that shows all investment offers on a
        specific campaign.
        Shows a "Select campaign" alert of no campaign was selected before the button was pressed.
        """
        if self.table.selectedIndexes():
            # selected_data = map((lambda item: item.data()), self.table.selectedIndexes())
            selected_row = self.table.selectedIndexes()[0].row()
            self.mainwindow.navigation.switch_to_campaign_bids(self.content[selected_row][0].id)
        else:
            self.mainwindow.show_dialog("Select campaign", 'No campaigns have been selected.')

    def set_filters(self):
        self.mainwindow.filter_table(self.table,
                                     self.mainwindow.openmarket_search_lineedit.text(),
                                     1,
                                     self.mainwindow.openmarket_min_amount_lineedit.text(),
                                     self.mainwindow.openmarket_max_amount_lineedit.text(),
                                     2,
                                     self.mainwindow.openmarket_interest1_lineedit.text(),
                                     self.mainwindow.openmarket_interest2_lineedit.text(),
                                     3,
                                     self.mainwindow.openmarket_duration1_lineedit.text(),
                                     self.mainwindow.openmarket_duration2_lineedit.text())
