import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from market.views.main_view import Ui_MainWindow
from marketGUI.market_app import MarketApplication
from market.api.api import MarketAPI


class OpenMarketController:
    def __init__(self, mainwindow):
        # self.mainwindow = Ui_MainWindow  # Comment before running
        self.mainwindow = mainwindow  # Uncomment before running
        self.selected_campaign = None
        self.mainwindow.openmarket_open_market_table.doubleClicked.connect(self.switch_to_view_campaign)
        self.mainwindow.openmarket_open_market_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def setup_view(self):
        self.selected_campaign = None
        content = self.mainwindow.api
        # chosen_index = self.fiplr1_loan_requests_table.selectedIndexes()[0].row()
        # chosen_request = content[chosen_index]     # index of the row
        pass

    def switch_to_view_campaign(self):
        if self.selected_campaign:
            self.mainwindow.stackedWidget.setCurrentWidget(self.mainwindow.fiplr1_page)


    def openmarket_view_open_market(self, fi_payload):
        # print self.openmarket_open_market_table.selectedIndexes()
        # TODO add new items in, instead of editing ones that exist.
        self.openmarket_open_market_table.setRowCount(len(fi_payload))
        for i in range(0, 1):
            # row = fi_payload[i]
            self.openmarket_open_market_table.item(i, 0).setText('Bouwerslaan ' + self.bplr_payload['house_number'] + ' , ' + self.bplr_payload['postal_code'])
            self.openmarket_open_market_table.item(i, 1).setText(str(self.bplr_payload['amount_wanted']))
            self.openmarket_open_market_table.item(i, 2).setText(str(fi_payload['interest_rate']))
            self.openmarket_open_market_table.item(i, 3).setText(str(fi_payload['duration']))


    def openmarket_view_campaign(self):
        address = 'Bouwerslaan ' + self.bplr_payload['house_number'] + ' , ' + self.bplr_payload['postal_code']
        self.icb_property_address_lineedit.setText(address)
        # self.icb_current_bids_table.setRowCount(0)
        self.next_screen()

    def icb_place_bid(self):
        # row_count = self.icb_current_bids_table.rowCount()
        # self.icb_current_bids_table.insertRow(row_count)
        # print row_count
        self.icb_current_bids_table.item(0, 0).setText(self.icb_amount_lineedit.text())
        self.icb_current_bids_table.item(0, 1).setText(self.icb_duration_lineedit.text())
        self.icb_current_bids_table.item(0, 2).setText(self.icb_interest_lineedit.text())
