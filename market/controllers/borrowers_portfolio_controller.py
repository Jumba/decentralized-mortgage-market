from PyQt5.QtWidgets import *

from market.models.loans import Mortgage, Investment


class BorrowersPortfolioController:
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow  # Uncomment before running
        self.accepted_loans = None
        self.pending_loans = None
        self.accepted_table = self.mainwindow.bp_ongoing_loans_table
        self.pending_table = self.mainwindow.bp_open_offers_table
        self.mainwindow.bp_accept_pushbutton.clicked.connect(self.accept_offer)
        self.mainwindow.bp_reject_pushbutton.clicked.connect(self.reject_offer)

    def setup_view(self):
        self.accepted_table.setRowCount(0)
        self.pending_table.setRowCount(0)
        self.accepted_loans = self.mainwindow.api.load_borrowers_loans(self.mainwindow.app.user)
        self.pending_loans = self.mainwindow.api.load_borrowers_offers(self.mainwindow.app.user)
        for loan in self.accepted_loans:
            if isinstance(loan, Mortgage):
                self.mainwindow.insert_row(self.accepted_table, [loan.amount, loan.interest_rate,
                                                                 loan.default_rate, loan.duration,
                                                                 loan.type])
            elif isinstance(loan, Investment):
                self.mainwindow.insert_row(self.accepted_table, [loan.amount, loan.interest_rate,
                                                                 ' ', loan.duration, loan.type])
        for offer in self.pending_loans:
            if isinstance(offer, Mortgage):
                self.mainwindow.insert_row(self.pending_table, [offer.amount, offer.interest_rate,
                                                                offer.default_rate, offer.duration,
                                                                offer.type])
            elif isinstance(offer, Investment):
                self.mainwindow.insert_row(self.pending_table, [offer.amount, offer.interest_rate,
                                                                ' ', offer.duration, offer.type])

    def accept_offer(self):
        try:
            selected_row = self.pending_table.selectedIndexes()[0].row()
            offer = self.pending_loans[selected_row]

            if offer.type == Investment.type:
                self.mainwindow.api.accept_investment_offer(self.mainwindow.app.user, {'investment_id': offer.id})
            else:
                self.mainwindow.api.accept_mortgage_offer(self.mainwindow.app.user, {'mortgage_id': offer.id})
            self.mainwindow.show_dialog('Offer accepted',
                                        'You have accepted the chosen offer')
            self.setup_view()

        except IndexError:
            self.mainwindow.show_dialog("Select offer", 'No offers have been selected.')

    def reject_offer(self):
        try:
            selected_row = self.pending_table.selectedIndexes()[0].row()
            offer = self.pending_loans[selected_row]

            if offer.type == Investment.type:
                self.mainwindow.api.reject_investment_offer(self.mainwindow.app.user, {'investment_id': offer.id})
            else:
                self.mainwindow.api.reject_mortgage_offer(self.mainwindow.app.user, {'mortgage_id': offer.id})
            self.mainwindow.show_dialog('Offer rejected',
                                        'You have rejected the chosen offer')
            self.setup_view()
        except IndexError:
            self.mainwindow.show_dialog("Select offer", 'No offers have been selected.')
