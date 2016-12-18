import sys
from uuid import UUID

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from market.models.loans import Campaign
from market.models.role import Role
from market.models.user import User
from market.views.main_view import Ui_MainWindow
from marketGUI.market_app import MarketApplication
from market.api.api import MarketAPI


class BorrowersPortfolioController:
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow  # Uncomment before running
        self.accepted_loans = None
        self.pending_loans = None
        self.accepted_table = self.mainwindow.bp_ongoing_loans_table
        self.pending_table = self.mainwindow.bp_open_offers_table
        self.mainwindow.bp_accept_pushbutton.clicked.connect(self.accept_loan)
        self.mainwindow.bp_reject_pushbutton.clicked.connect(self.reject_loan)

    def setup_view(self):
        self.testdata()
        self.accepted_table.setRowCount(0)
        self.pending_table.setRowCount(0)
        self.accepted_loans = self.mainwindow.api.load_borrowers_loans(self.mainwindow.app.user)
        self.pending_loans = self.mainwindow.api.load_borrowers_offers(self.mainwindow.app.user)
        for loan in self.accepted_loans:
            self.mainwindow.insert_row(self.accepted_table, [loan.amount, loan.interest_rate, loan.default_rate, loan.duration, loan._type])
        for loan in self.pending_loans:
            self.mainwindow.insert_row(self.accepted_table, [loan.amount, loan.interest_rate, loan.default_rate, loan.duration, loan._type])

    def accept_loan(self):
        if self.pending_table.selectedIndexes():
            # selected_data = map((lambda item: item.data()), self.table.selectedIndexes())
            selected_row = self.pending_table.selectedIndexes()[0].row()
            self.accept_offer(self.accepted_loans[selected_row].id)

    def reject_loan(self):
        if self.pending_table.selectedIndexes():
            # selected_data = map((lambda item: item.data()), self.table.selectedIndexes())
            selected_row = self.pending_table.selectedIndexes()[0].row()
            self.reject_offer(self.accepted_loans[selected_row].id)

    def accept_offer(self, loan):
        if loan._type == 'investment':
            self.mainwindow.api.accept_investment_offer(loan.id)
        else:
            self.mainwindow.api.accept_mortgage_offer(loan.id)
        QMessageBox.about(self.mainwindow, 'Loan accepted',
                          'You have accepted the chosen loan')
        self.setup_view()

    def reject_offer(self, loan):
        if loan._type == 'investment':
            self.mainwindow.api.reject_investment_offer(loan.id)
        else:
            self.mainwindow.api.reject_mortgage_offer(loan.id)
        QMessageBox.about(self.mainwindow, 'Loan rejected',
                          'You have rejected the chosen loan')
        self.setup_view()


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


        borrower = self.mainwindow.app.user
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

