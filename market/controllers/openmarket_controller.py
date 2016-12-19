from datetime import datetime
from uuid import UUID

from PyQt5.QtWidgets import *

from market.models.loans import Campaign
from market.models.role import Role
from market.models.user import User


class OpenMarketController:
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.content = None
        self.table = self.mainwindow.openmarket_open_market_table
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.doubleClicked.connect(self.view_campaign)
        self.mainwindow.openmarket_view_loan_bids_pushbutton.clicked.connect(self.view_campaign)

    def setup_view(self):
        self.table.setRowCount(0)
        self.content = self.mainwindow.api.load_open_market()
        for tpl in self.content:
            mortgage = tpl[0]
            campaign = tpl[1]
            house = tpl[2]
            row = []
            row.append(house.address + ' ' + house.house_number + ' , ' + house.postal_code)
            row.append(campaign.amount)
            row.append(mortgage.interest_rate)
            row.append(mortgage.duration)
            row.append((campaign.end_date - datetime.now()).days)
            row.append(mortgage.risk)
            self.mainwindow.insert_row(self.table, row)

    def view_campaign(self):
        if self.table.selectedIndexes():
            # selected_data = map((lambda item: item.data()), self.table.selectedIndexes())
            selected_row = self.table.selectedIndexes()[0].row()
            self.mainwindow.navigation.switch_to_campaign_bids(self.content[selected_row][0].id)
