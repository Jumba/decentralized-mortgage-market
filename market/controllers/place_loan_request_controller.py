import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from market.views import login
from marketGUI.market_app import MarketApplication
import main_view_controller


class PlaceLoanRequestController():
    def __init__(self, mainwindow):
        print 'init'
        self.bplr_submit_button.clicked.connect(self.submit_loan_request)

    def submit_loan_request(self):
        print 'submit_loan_request'
        fields = {'postal_code': self.mainwindow.bplr_postcode_lineedit,
                  'house_number': self.mainwindow.bplr_housenumber_lineedit,
                  'price': self.mainwindow.bplr_house_price_lineedit,
                  'description': self.mainwindow.bplr_description_textedit,
                  'amount_wanted': self.mainwindow.bplr_amount_wanted_lineedit}
        banks = [self.mainwindow.bplr_bank1_checkbox, self.mainwindow.bplr_bank2_checkbox, self.mainwindow.bplr_bank3_checkbox,
                 self.mainwindow.bplr_bank4_checkbox]
        banks_ids = ['1', '2', '3', '4']
        banks_payload = []

        pointer = 0
        for obj in banks:
            if obj.checkState():
                banks_payload += banks_ids(pointer)
            pointer += 1
        print banks_payload

        if self.mainwindow.bplr_linear_radiobutton.isChecked():
            fields['mortgage_type'] = 0
        else:
            fields['mortgage_type'] = 1