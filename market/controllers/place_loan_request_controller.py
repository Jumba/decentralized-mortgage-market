from PyQt5.QtWidgets import *
from market import Global

class PlaceLoanRequestController:
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.payload = {}
        self.mainwindow.bplr_submit_pushbutton.clicked.connect(self.submit_loan_request)
        self.banks_ids = Global.BANKS.values()

    def setup_view(self):
        pass

    def submit_loan_request(self):
        try:
            self.payload = {'address': str(self.mainwindow.bplr_address_lineedit.text()),
                            'postal_code': str(self.mainwindow.bplr_postcode_lineedit.text()),
                            'house_number': str(self.mainwindow.bplr_housenumber_lineedit.text()),
                            'price': int(self.mainwindow.bplr_house_price_lineedit.text()),
                            'amount_wanted': int(self.mainwindow.bplr_amount_wanted_lineedit.text()),
                            'description': unicode(self.mainwindow.bplr_description_textedit.toPlainText()),
                            'seller_phone_number': str(self.mainwindow.bplr_seller_phone_number_lineedit.text()),
                            'seller_email': str(self.mainwindow.bplr_seller_email_lineedit.text()),
                            'house_link': str(self.mainwindow.bplr_house_link_lineedit.text())
                            }
            banks = [self.mainwindow.bplr_bank1_checkbox, self.mainwindow.bplr_bank2_checkbox,
                     self.mainwindow.bplr_bank3_checkbox,
                     self.mainwindow.bplr_bank4_checkbox]

            checked_banks = []
            pointer = 0

            # Check which banks were chosen
            for obj in banks:
                if obj.checkState():
                    checked_banks.append(self.banks_ids[pointer])
                pointer += 1

            if not checked_banks:
                raise ValueError
            self.payload['banks'] = checked_banks

            # Check the chosen mortgage type
            self.payload['mortgage_type'] = 1
            if self.mainwindow.bplr_linear_radiobutton.isChecked():
                self.payload['mortgage_type'] = 0

            if self.mainwindow.api.create_loan_request(self.mainwindow.app.user, self.payload):
                self.mainwindow.show_dialog("Loan request created", 'Your loan request has been sent.')
            else:
                self.mainwindow.show_dialog("Loan request error", 'You can only have a single loan request.')
        except ValueError:
            self.mainwindow.show_dialog("Loan request error", 'You didn\'t enter the required information.')
