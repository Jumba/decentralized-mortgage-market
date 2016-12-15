import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from market.views.main_view import Ui_MainWindow
from marketGUI.market_app import MarketApplication
from market.api.api import MarketAPI


class ProfileController:
    def __init__(self, mainwindow):
        # self.mainwindow = Ui_MainWindow  # Comment before running
        self.mainwindow = mainwindow  # Uncomment before running
        self.current_profile = None
        # check if the profile already exists
        # self.user = self.mainwindow.app.user


    def setup_view(self):
        self.current_profile = self.mainwindow.api.load_profile(self.mainwindow.app.user)
        print 'Current profile: '
        print self.current_profile
        self.mainwindow.profile_save_pushbutton.clicked.connect(self.save_form)

    def save_form(self):
        # role = 0
        # if self.mainwindow.profile_borrower_radiobutton.isChecked():
        #     role = 1
        # else:
        #     role = 2

        self.payload = {'role': 2, 'first_name': str(self.mainwindow.profile_firstname_lineedit.text()),
                             'last_name': str(self.mainwindow.profile_lastname_lineedit.text()),
                             'email': str(self.mainwindow.profile_email_lineedit.text()),
                             'iban': str(self.mainwindow.profile_iban_lineedit.text()),
                             'phonenumber': str(self.mainwindow.profile_phonenumber_lineedit.text())}

        # for key in self._basic_forms:
        #     payload[key] = self._basic_forms[key].text()

        if self.mainwindow.profile_borrower_radiobutton.isChecked():
            self.payload['role'] = 1
            self.payload['current_postalcode'] = str(self.mainwindow.profile_postcode_lineedit.text())
            self.payload['current_housenumber'] = str(self.mainwindow.profile_housenumber_lineedit.text()) # missing 'documents_list': self.documentsTable
            self.payload['documents_list'] = []
        # print self.payload
        # print 'creating profile:'
        if self.mainwindow.api.create_profile(self.mainwindow.app.user, self.payload):
            QMessageBox.about(self.mainwindow, "My message box", 'mitnaka')
        # print 'check if the profile has been added:'
        # print self.mainwindow.api.load_profile(self.mainwindow.app.user)
