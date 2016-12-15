import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from market.views import login
from marketGUI.market_app import MarketApplication
import main_view_controller


class PlaceLoanRequestController:
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.payload = {}

    def setup_view(self):
        self.mainwindow.bplr_submit_button.clicked.connect(self.submit_loan_request)

    def submit_loan_request(self):
        self.payload = {'postal_code': str(self.mainwindow.bplr_postcode_lineedit.text()),
                  'house_number': str(self.mainwindow.bplr_housenumber_lineedit.text()),
                  'price': int(self.mainwindow.bplr_house_price_lineedit.text()),
                  'amount_wanted': int(self.mainwindow.bplr_amount_wanted_lineedit.text())}
        banks = [self.mainwindow.bplr_bank1_checkbox, self.mainwindow.bplr_bank2_checkbox,
                 self.mainwindow.bplr_bank3_checkbox,
                 self.mainwindow.bplr_bank4_checkbox]
        banks_ids = ['1', '2', '3', '4']
        checked_banks = []

        # # Get all the inputs
        # for key in fields:
        #     self.payload[key] = fields[key]

        #which banks were chosen
        pointer = 0
        for obj in banks:
            if obj.checkState():
                checked_banks += banks_ids[pointer]
                print 'Checked banks',
                print checked_banks
            pointer += 1
        # self.bplr_payload['banks'] = checked_banks
        # print ' use this '
        # print self.user_bank.user_key
        # self.bplr_payload['banks'] = [self.user_bank.user_key]
        self.payload['banks'] = checked_banks


        #check the chosen mortgage type
        self.payload['mortgage_type'] = 1
        if self.mainwindow.bplr_linear_radiobutton.isChecked():
            self.payload['mortgage_type'] = 0

        self.payload['description'] = unicode(self.mainwindow.bplr_description_textedit.toPlainText())

        # remove during refactor
        # self.setCurrentIndex(4)
        print self.payload
        print 'creating loan request'
        if self.mainwindow.api.create_loan_request(self.mainwindow.app.user, self.payload):
            QMessageBox.about(self.mainwindow, "My message box", 'Loan request created.')
