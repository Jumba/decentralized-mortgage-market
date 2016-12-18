import sys
from datetime import date, datetime
from uuid import UUID

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from market.models.loans import LoanRequest, Campaign
from market.models.role import Role
from market.models.user import User
from market.views.main_view import Ui_MainWindow
from marketGUI.market_app import MarketApplication
from market.api.api import MarketAPI


class OpenMarketController:
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow  # Uncomment before running
        self.content = None
        self.table = self.mainwindow.openmarket_open_market_table
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.doubleClicked.connect(self.view_campaign)
        self.mainwindow.openmarket_view_loan_bids_pushbutton.clicked.connect(self.view_campaign)
        self.testdata()
        # self.setup_view()
        # self.mainwindow.stackedWidget.setCurrentWidget(self.mainwindow.openmarket_page)
        # self.setup_view()
        # self.mainwindow.stackedWidget.setCurrentWidget(self.s)
        # QTableWidget.horizontalHeader()
        # QTableWidget.setHorizontalHeader()

        # chosen_index = self.fiplr1_loan_requests_table.selectedIndexes()[0].row()
        # chosen_request = content[chosen_index]     # index of the row

    def reset_table(self):
        self.table.setRowCount(0)

    def setup_view(self):
        self.reset_table()
        # content = [[][][]]
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


    def testdata(self):
        self.api = self.mainwindow.api
        self.payload_loan_request1 = {'postal_code': '1210 BV', 'house_number': '89', 'address': 'Randstraat',
                                      'price': 150000, 'role': 1,
                                      'house_id': UUID('b97dfa1c-e125-4ded-9b1a-5066462c520c'), 'mortgage_type': 1,
                                      'banks': [], 'description': unicode('La la la'),
                                      'amount_wanted': 200000, 'house_link': 'http://www.myhouseee.com/',
                                      'seller_phone_number': '0612345678', 'seller_email': 'seller1@gmail.com'}
        self.payload_loan_request2 = {'postal_code': '1011 TV', 'house_number': '55', 'address': 'Randstraat',
                                      'price': 160000, 'role': 1,
                                      'house_id': UUID('b97dfa1c-e125-4ded-9b1a-5066462c520c'), 'mortgage_type': 1,
                                      'banks': [], 'description': unicode('Ho ho ho merry christmas'),
                                      'amount_wanted': 250000, 'house_link': 'http://www.myhouseee.com/',
                                      'seller_phone_number': '0612345678', 'seller_email': 'seller1@gmail.com'}
        self.payload_loan_request = {'house_id': UUID('b97dfa1c-e125-4ded-9b1a-5066462c520c'), 'mortgage_type': 1,
                                     'banks': [],
                                     'description': unicode('I want to buy a house'), 'amount_wanted': 123456,
                                     'postal_code': '1111AA', 'house_number': '11', 'address': 'Randstraat',
                                     'price': 123456,
                                     'house_link': 'http://www.myhouseee.com/', 'seller_phone_number': '0612345678',
                                     'seller_email': 'seller1@gmail.com'}
        self.payload_mortgage = {'house_id': UUID('b97dfa1c-e125-4ded-9b1a-5066462c520c'), 'mortgage_type': 1, 'amount': 123000, 'interest_rate' : 5.5, 'max_invest_rate' : 7.0, 'default_rate' : 9.0, 'duration' : 30, 'risk' : 'hi', 'investors' : []}


        borrower, _, _ = self.api.create_user()
        role_id = Role(1)
        borrower.role_id = role_id
        self.api.db.put(User._type, borrower.id, borrower)

        bank, _, _ = self.api.create_user()
        role_id = Role(3)
        bank.role_id = role_id
        self.api.db.put(User._type, bank.id, bank)

        # Create loan request
        self.payload_loan_request['user_key'] = borrower.id  # set user_key to the borrower's public key
        self.payload_loan_request['banks'] = [bank.id]
        loan_request = self.api.create_loan_request(borrower, self.payload_loan_request)

        # Set payload
        self.payload_mortgage['user_key'] = borrower.id
        self.payload_mortgage['request_id'] = loan_request.id
        self.payload_mortgage['house_id'] = self.payload_loan_request['house_id']
        self.payload_mortgage['mortgage_type'] = self.payload_loan_request['mortgage_type']

        # Accept the loan request
        accepted_loan_request, mortgage = self.api.accept_loan_request(bank, self.payload_mortgage)

        # Accept mortgage offer
        self.payload_mortgage['mortgage_id'] = mortgage.id
        self.api.accept_mortgage_offer(borrower, self.payload_mortgage)

        # Get the list of active campaigns
        open_market = self.api.load_open_market()

        # Check if the open market is not empty

        # Set the status of the campaign to completed
        campaigns = self.api.db.get_all(Campaign._type)
