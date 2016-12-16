from PyQt5.QtWidgets import *
from market.views.main_view import Ui_MainWindow


class PlaceLoanRequestController:
    def __init__(self, mainwindow):
        # self.mainwindow = Ui_MainWindow  # Comment before running
        self.mainwindow = mainwindow  # Uncomment before running
        self.payload = {}
        self.mainwindow.bplr_submit_button.clicked.connect(self.submit_loan_request)

    def setup_view(self):
        pass

    def submit_loan_request(self):
        self.payload = {'postal_code': str(self.mainwindow.bplr_postcode_lineedit.text()),
                        'house_number': str(self.mainwindow.bplr_housenumber_lineedit.text()),
                        'price': int(self.mainwindow.bplr_house_price_lineedit.text()),
                        'amount_wanted': int(self.mainwindow.bplr_amount_wanted_lineedit.text()),
                        'description': unicode(self.mainwindow.bplr_description_textedit.toPlainText()),
                        # TODO the following two fields are subject to change
                        'seller_phone_number': str(self.mainwindow.bplr_seller_phone_number_lineedit.text()),
                        'seller_email': str(self.mainwindow.bplr_seller_email_lineedit.text())
                        }
        banks = [self.mainwindow.bplr_bank1_checkbox, self.mainwindow.bplr_bank2_checkbox,
                 self.mainwindow.bplr_bank3_checkbox,
                 self.mainwindow.bplr_bank4_checkbox]
        banks_ids = self.mainwindow.bank_ids

        checked_banks = []
        pointer = 0
        #which banks were chosen
        for obj in banks:
            if obj.checkState():
                checked_banks.append(banks_ids[pointer])
            pointer += 1

        self.payload['banks'] = checked_banks

        #check the chosen mortgage type
        self.payload['mortgage_type'] = 1
        if self.mainwindow.bplr_linear_radiobutton.isChecked():
            self.payload['mortgage_type'] = 0

        if self.mainwindow.api.create_loan_request(self.mainwindow.app.user, self.payload):
            QMessageBox.about(self.mainwindow, "Loan request created", 'Your loan request has been sent!')
        else:
            QMessageBox.about(self.mainwindow, "Loan request failed", 'You can only have a single loan request')
