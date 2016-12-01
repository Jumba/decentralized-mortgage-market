import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from market.views import profile_view
from market.api.api import MarketAPI
from marketGUI.market_app import MarketApplication


class ProfileController(QMainWindow, profile_view.Ui_MainWindow):
    def __init__(self, parent=None, app=None):
        super(ProfileController, self).__init__(parent)
        self.setupUi(self)
        self.app = app
        self.saveButton.clicked.connect(self.save_form)

        self._basic_forms = {'first_name': self.firstNameField, 'last_name': self.lastNameField, 'email': self.emailAddressField, 'iban': self.IBANField, 'phonenumber': self.telNumberField};
        self._borrower_forms = {'current_postalcode': self.curPostalCodeField, 'current_housenumber': self.curHouseNumberField}; #missing 'documents_list': self.documentsTable

    def save_form(self):
        payload = {'role': 'INVESTOR'}
        for key in self._basic_forms:
            payload[key] = self._basic_forms[key].text()

        if self.radioButtonBorrower.isChecked():
            for key in self._borrower_forms:
                payload[key] = self._borrower_forms[key].text()

        print payload
        # MarketAPI.create_profile(self.app.user, payload)

        print 'saved'

def main():
    app = MarketApplication(sys.argv)
    form = ProfileController(app=app)
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
