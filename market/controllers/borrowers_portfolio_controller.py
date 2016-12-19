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
