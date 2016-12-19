from PyQt5.QtWidgets import QMessageBox


class PendingLoanRequests2Controller:
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.loan_request_id = None

        # Add listener to the 'accept' and 'reject' buttons
        self.mainwindow.fiplr2_accept_pushbutton.clicked.connect(self.accept_request)
        self.mainwindow.fiplr2_reject_pushbutton.clicked.connect(self.reject_request)

    def setup_view(self, loan_request_id):
        self.loan_request_id = loan_request_id
        [loan_request, borrower_profile, house] = self.mainwindow.api.load_single_loan_request({'loan_request_id' : loan_request_id})

        # Insert personal information
        self.mainwindow.fiplr2_firstname_lineedit.setText(str(borrower_profile.first_name))
        self.mainwindow.fiplr2_lastname_lineedit.setText(str(borrower_profile.last_name))
        self.mainwindow.fiplr2_address_lineedit.setText(str(borrower_profile.current_address) + ' '
                                                    + str(borrower_profile.current_house_number) + ', '
                                                    + str(borrower_profile.current_postal_code))
        self.mainwindow.fiplr2_phonenumber_lineedit.setText(str(borrower_profile.phone_number))
        self.mainwindow.fiplr2_email_lineedit.setText(str(borrower_profile.email))
        # TODO Add risk rating when it has been implemented

        # Insert mortgage request information
        self.mainwindow.fiplr2_property_address_lineedit.setText(str(house.postal_code) + ', '
                                                                 + str(house.house_number))
        self.mainwindow.fiplr2_loan_amount_lineedit.setText(str(loan_request.amount_wanted))

        mortgage_type = ''
        if loan_request.mortgage_type == 1:
            mortgage_type = 'Linear'
        elif loan_request.mortgage_type == 2:
            mortgage_type = 'Fixed-Rate'

        self.mainwindow.fiplr2_mortgage_type_lineedit.setText(mortgage_type)
        self.mainwindow.fiplr2_property_value_lineedit.setText(str(house.price))
        self.mainwindow.fiplr2_description_textedit.setText(str(loan_request.description))

    def reject_request(self):
        # Reject the loan request
        self.mainwindow.api.reject_loan_request(self.mainwindow.app.user, {'request_id' : self.loan_request_id})
        QMessageBox.about(self.mainwindow, "Request rejected", 'This loan request has been rejected.')
        # Switch back to the pending loan requests 1 screen
        self.mainwindow.navigation.switch_to_fiplr()

    def accept_request(self):
        # TODO Add max_invest_rate and risk to the payload when they are implemented
        try:
            # Create payload
            payload = {'request_id' : self.loan_request_id, 'amount' : self.mainwindow.fiplr2_offer_amount_lineedit.text(),
                       'interest_rate' : self.mainwindow.fiplr2_offer_interest_lineedit.text(), 'max_invest_rate' : 0,
                       'default_rate' : self.mainwindow.fiplr2_default_rate_lineedit,
                       'duration' : self.mainwindow.fiplr2_loan_duration_lineedit, 'risk' : ' '}

            # Check if all fields are filled out
            for _, value in payload.iteritems():
                if value == '':
                    raise ValueError

            # Accept the loan request
            self.mainwindow.api.accept_loan_request(self.mainwindow.app.user, payload)
            QMessageBox.about(self.mainwindow, "Request accepted", 'This loan request has been accepted.')

            # Switch back to the pending loan requests 1 screen
            self.mainwindow.navigation.switch_to_fiplr()
        except ValueError:
            QMessageBox.about(self.mainwindow, "Loan request error", 'You didn\'t enter all of the required '
                                                                    'information.')
