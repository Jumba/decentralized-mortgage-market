from market import Global
from market.api.api import STATUS
from market.models.loans import Mortgage, Investment, Campaign, LoanRequest


class BorrowersPortfolioController:
    """
    Create a BorrowersPortfolioController object that performs tasks on the Borrower's Portfolio section of the gui.
    Takes a MainWindowController object during construction.
    """
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.accepted_loans = None
        self.pending_loans = None
        self.accepted_table = self.mainwindow.bp_ongoing_loans_table
        self.pending_table = self.mainwindow.bp_open_offers_table
        self.mainwindow.bp_accept_pushbutton.clicked.connect(self.accept_offer)
        self.mainwindow.bp_reject_pushbutton.clicked.connect(self.reject_offer)

    def setup_view(self):
        """
        Setup the portfolio screen with up-to-date data.
        """
        # Clear the table
        self.accepted_table.setRowCount(0)
        self.pending_table.setRowCount(0)

        # Retrieve the loans
        self.accepted_loans = self.mainwindow.api.load_borrowers_loans(self.mainwindow.app.user)
        self.pending_loans = self.mainwindow.api.load_borrowers_offers(self.mainwindow.app.user)

        # Fill the table with loans
        self.add_accepted_loans()
        self.add_pending_loans()

        # Update the borrower's loan status
        self.add_loan_status()

    def add_loan_status(self):
        """
        Updates loan status label
        """
        loan = self.mainwindow.api.load_borrowers_loan_status(self.mainwindow.app.user)

        if isinstance(loan, Campaign):
            if loan.completed:
                self.mainwindow.bp_status_label.setText('You currently have no active loan request.')
            else:
                self.mainwindow.bp_status_label.setText('You currently have a running campaign. Amount needed: ' +
                                                        str(loan.amount) + u' \u20ac')
        elif isinstance(loan, LoanRequest):
            self.mainwindow.bp_status_label.setText('You currently have a pending loan request.')
        else:
            self.mainwindow.bp_status_label.setText('You currently have no active loan request.')

    def add_accepted_loans(self):
        """
        Adds the accepted loans to the table.
        """
        for loan, profile in self.accepted_loans:
            default_rate = ' '
            name = ' '
            iban = ' '

            if isinstance(loan, Mortgage):
                default_rate = loan.default_rate

                for bank, bank_id in Global.BANKS.iteritems():
                    if bank_id == loan.bank:
                        name = bank
            elif isinstance(loan, Investment):
                name = profile.first_name + ' ' + profile.last_name
                iban = profile.iban

            self.mainwindow.insert_row(self.accepted_table, [loan.amount, loan.interest_rate,
                                                             default_rate, loan.duration,
                                                             loan.type, name, iban])

    def add_pending_loans(self):
        """
        Adds the pending loans to the table.
        """
        for offer in self.pending_loans:
            if isinstance(offer, Mortgage):
                bank_name = ' '

                for bank, bank_id in Global.BANKS.iteritems():
                    if bank_id == offer.bank:
                        bank_name = bank

                self.mainwindow.insert_row(self.pending_table, [offer.amount, offer.interest_rate,
                                                                offer.default_rate, offer.duration,
                                                                offer.type, bank_name])
            elif isinstance(offer, Investment):
                self.mainwindow.insert_row(self.pending_table, [offer.amount, offer.interest_rate,
                                                                ' ', offer.duration, offer.type, ' '])

    def accept_offer(self):
        """
        Accept a loan offer or investment.

        Shows a "Offer accepted" alert if accepting the offer was successful.
        Shows a "Select offer" alert if the user has not selected any offers from the table.
        """
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
        """
        Reject a loan offer or investment.

        Shows a "Offer rejected" alert if rejecting the offer was successful.
        Shows a "Select offer" alert if the user has not selected any offers from the table.
        """
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
