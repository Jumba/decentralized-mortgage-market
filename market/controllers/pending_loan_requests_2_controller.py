import ntpath
import os
import subprocess
import sys

from glob import glob
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QTableWidgetItem


class PendingLoanRequests2Controller:
    """
    Create a PendingLoanRequests2Controller object that performs tasks on the Pending Loan Request 2 section of the gui.
    Takes a MainWindowController object during construction.
    """
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.table = self.mainwindow.fiplr2_documents_table
        self.loan_request_id = None

        # Add listener to the 'accept' and 'reject' buttons
        self.mainwindow.fiplr2_accept_pushbutton.clicked.connect(self.accept_request)
        self.mainwindow.fiplr2_reject_pushbutton.clicked.connect(self.reject_request)

    def setup_view(self, loan_request_id):
        """
        Setup the view to show in depth information about the loan request and the user that requested it.
        :param loan_request_id: The UUID of the loan request
        """
        self.loan_request_id = loan_request_id
        [loan_request, borrower_profile, house] = self.mainwindow.api.load_single_loan_request(
            {'loan_request_id': loan_request_id})

        # Insert personal information
        self.mainwindow.fiplr2_firstname_lineedit.setText(str(borrower_profile.first_name))
        self.mainwindow.fiplr2_lastname_lineedit.setText(str(borrower_profile.last_name))
        self.mainwindow.fiplr2_address_lineedit.setText(str(borrower_profile.current_address) + ' '
                                                        + str(borrower_profile.current_house_number) + ', '
                                                        + str(borrower_profile.current_postal_code))
        self.mainwindow.fiplr2_phonenumber_lineedit.setText(str(borrower_profile.phone_number))
        self.mainwindow.fiplr2_email_lineedit.setText(str(borrower_profile.email))

        # Insert mortgage request information
        self.mainwindow.fiplr2_property_address_lineedit.setText(str(house.address) + ' ' + str(house.house_number)
                                                                 + ', ' + str(house.postal_code))
        self.mainwindow.fiplr2_loan_amount_lineedit.setText(str(loan_request.amount_wanted))

        mortgage_type = ''
        if loan_request.mortgage_type == 1:
            mortgage_type = 'Linear'
        elif loan_request.mortgage_type == 2:
            mortgage_type = 'Fixed-Rate'

        self.mainwindow.fiplr2_mortgage_type_lineedit.setText(mortgage_type)
        self.mainwindow.fiplr2_property_value_lineedit.setText(str(house.price))
        self.mainwindow.fiplr2_description_textedit.setText(str(loan_request.description))

        documents = glob(os.getcwd() + '/resources/received/'+str(loan_request_id)+'/*.pdf')
        for i in range(0, len(documents)):
            self.table.insertRow(i)
            edit_button = QPushButton('View')
            edit_button.clicked.connect(self.view_file)
            edit_button.filepath = documents[i]
            self.table.setItem(i, 0, QTableWidgetItem(str(ntpath.basename(documents[i]))))
            self.table.setCellWidget(i, 1, edit_button)

    def view_file(self):
        filepath = self.mainwindow.sender().filepath
        if sys.platform.startswith('darwin'):
            subprocess.call(('open', filepath))
        elif os.name == 'nt':
            os.startfile(filepath)
        elif os.name == 'posix':
            subprocess.call(('xdg-open', filepath))

    def reject_request(self):
        """
        Reject the shown loan request. Redirects the user back to Pending Loan Requests 1.
        """
        # Reject the loan request
        self.mainwindow.api.reject_loan_request(self.mainwindow.app.user, {'request_id': self.loan_request_id})
        self.mainwindow.show_dialog("Request rejected", 'This loan request has been rejected.')
        # Switch back to the pending loan requests 1 screen
        self.mainwindow.navigation.switch_to_fiplr()

    def accept_request(self):
        """
        Accept the shown loan request.
        Shows "Request accepted" if the form was filled in correctly.
        Shows "Loan request error"" if the form was not filled in correctly.
        """
        try:
            # Create payload
            payload = {'request_id': self.loan_request_id,
                       'amount': int(self.mainwindow.fiplr2_offer_amount_lineedit.text()),
                       'interest_rate': float(self.mainwindow.fiplr2_offer_interest_lineedit.text()),
                       'max_invest_rate': 0.0,
                       'default_rate': float(self.mainwindow.fiplr2_default_rate_lineedit.text()),
                       'duration': int(self.mainwindow.fiplr2_loan_duration_lineedit.text()),
                       'risk': ' '}

            # Check if all fields are filled out
            for _, value in payload.iteritems():
                if value == '':
                    raise ValueError

            # Accept the loan request
            self.mainwindow.api.accept_loan_request(self.mainwindow.app.user, payload)
            self.mainwindow.show_dialog("Request accepted", 'This loan request has been accepted.')

            # Switch back to the pending loan requests 1 screen
            self.mainwindow.navigation.switch_to_fiplr()
        except ValueError:
            self.mainwindow.show_dialog("Loan request error", 'You didn\'t enter all of the required information.')
