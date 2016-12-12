import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from market.database.backends import MemoryBackend
from market.database.database import MockDatabase
from market.views import main_view
from marketGUI.market_app import MarketApplication
from market.api.api import MarketAPI
import login_controller


class MainWindowController(QMainWindow, main_view.Ui_MainWindow):
    def __init__(self, parent=None, app=None):
        super(MainWindowController, self).__init__(parent)
        self.database = MockDatabase(MemoryBackend())
        self.api = MarketAPI(self.database)
        self.mainwindow = self #to make moving to another class easier
        self.app = app
        self.bplr_payload = {}
        self.setupUi(self)
        self.set_navigation()
        self.bplr_submit_button.clicked.connect(self.bplr_submit_loan_request)
        self.fiplr1_loan_requests_table.doubleClicked.connect(self.fiplr2_view_loan_request)
        self.openmarket_open_market_table.doubleClicked.connect(self.openmarket_view_campaign)
        self.fiplr1_view_loan_request_pushbutton.clicked.connect(self.fiplr2_view_loan_request)
        self.fiplr2_accept_pushbutton.clicked.connect(self.fiplr2_accept_loan_request)
        self.fiplr2_reject_pushbutton.clicked.connect(self.fiplr2_reject_loan_request)
        self.icb_place_bid_pushbutton.clicked.connect(self.icb_place_bid)
        self.setupObjects()
        self.login_controller = login_controller.LoginController(self)

        self.stackedWidget.setCurrentIndex(0)
        print self.stackedWidget.count()

    def bplr_submit_loan_request(self):
        fields = {'postal_code': str(self.mainwindow.bplr_postcode_lineedit.text()),
                  'house_number': str(self.mainwindow.bplr_housenumber_lineedit.text()),
                  'price': int(self.mainwindow.bplr_house_price_lineedit.text()),
                  'amount_wanted': int(self.mainwindow.bplr_amount_wanted_lineedit.text())}
        banks = [self.mainwindow.bplr_bank1_checkbox, self.mainwindow.bplr_bank2_checkbox,
                 self.mainwindow.bplr_bank3_checkbox,
                 self.mainwindow.bplr_bank4_checkbox]
        banks_ids = ['1', '2', '3', '4']
        checked_banks = []

        # Get all the inputs
        for key in fields:
            self.bplr_payload[key] = fields[key]

        #what banks were chosen
        pointer = 0
        for obj in banks:
            if obj.checkState():
                checked_banks += banks_ids[pointer]
            pointer += 1
        # self.bplr_payload['banks'] = checked_banks
        # print ' use this '
        # print self.user_bank.user_key
        self.bplr_payload['banks'] = [self.user_bank.user_key]

        #check the chosen mortgage type
        if self.mainwindow.bplr_linear_radiobutton.isChecked():
            self.bplr_payload['mortgage_type'] = 0
        else:
            self.bplr_payload['mortgage_type'] = 1

        self.bplr_payload['description'] = unicode(self.mainwindow.bplr_description_textedit.toPlainText())

        # remove during refactor
        # self.setCurrentIndex(4)
        print self.bplr_payload
        print 'creating loan request'
        print self.api.create_loan_request(self.user_borrower, self.bplr_payload)
        # self.bplr_payload = [self.bplr_payload]
        # self.fiplr1_populate_table(self.bplr_payload)
        self.fiplr1_load_all_pending_loan_requests()

    def fiplr1_load_all_pending_loan_requests(self):
        print 'Loading second screen!'
        # TODO request the contents with the uuid that is being returned from the following:
        # pop = self.api.load_all_loan_requests(self.user_bank)
        # print pop
        self.fiplr1_populate_table([self.bplr_payload])
        self.nextScreen()


    # method for populating the pending resquest table.
    def fiplr1_populate_table(self, payload):
        self.fiplr1_loan_requests_table.setRowCount(len(payload))
        for i in range(0, len(payload)):
            row = payload[i]
            self.fiplr1_loan_requests_table.item(i, 0).setText('Bouwerslaan ' + row['house_number']+' , '+row['postal_code'])
            self.fiplr1_loan_requests_table.item(i, 1).setText(str(row['mortgage_type']))
            self.fiplr1_loan_requests_table.item(i, 2).setText(str(row['amount_wanted']))
            self.fiplr1_loan_requests_table.item(i, 3).setText(str(row['price']))

    def fiplr2_view_loan_request(self):
        content = [self.bplr_payload]
        chosen_index = self.fiplr1_loan_requests_table.selectedIndexes()[0].row()
        chosen_request = content[chosen_index]     # index of the row
        print 'content'
        print content
        #personal information
        self.fiplr2_firstname_lineedit.setText(str(self.borrower_profile_payload['first_name']))
        self.fiplr2_lastname_lineedit.setText(str(self.borrower_profile_payload['last_name']))
        self.fiplr2_address_lineedit.setText(str('Laanlaan ' + self.borrower_profile_payload['current_housenumber'] + ' ' + self.borrower_profile_payload['current_postalcode']))
        self.fiplr2_phonenumber_lineedit.setText(str(self.borrower_profile_payload['phonenumber']))
        self.fiplr2_email_lineedit.setText(str(self.borrower_profile_payload['email']))

        #information about the request
        self.fiplr2_property_address_lineedit.setText('Bouwerslaan '+chosen_request['house_number']+' , '+chosen_request['postal_code'])
        # TODO rename the fiplr2_loan_amount_lineedit
        self.fiplr2_loan_amount_lineedit.setText(str(chosen_request['amount_wanted']))
        self.fiplr2_mortgage_type_lineedit.setText(str(chosen_request['mortgage_type']))
        self.fiplr2_property_value_lineedit.setText(str(chosen_request['price']))
        self.fiplr2_description_textedit.setText(str(chosen_request['description']))
        self.nextScreen()

    def fiplr2_accept_loan_request(self):
        # TODO api does not accept payload set by the bank in the fiplr2 screen
        bank_offer = {
            'amount': self.fiplr2_offer_amount_lineedit.text(),
            'interest_rate': self.fiplr2_offer_interest_lineedit.text(),
            'default_rate': self.fiplr2_default_rate_lineedit.text(),
            'duration': self.fiplr2_loan_duration_lineedit.text()
            # 'mortgage_id': self.fiplr2_loan_duration_lineedit.text()
        }
        self.openmarket_view_open_market(bank_offer)
        # TODO send the payload to the api
        # self.api.accept_loan_request()

    def fiplr2_reject_loan_request(self):
        self.previousScreen()
        # TODO do an actual reject with the api

    def openmarket_view_open_market(self, fi_payload):
        # print self.openmarket_open_market_table.selectedIndexes()
        # TODO add new items in, instead of editing ones that exist.
        self.openmarket_open_market_table.setRowCount(len(fi_payload))
        for i in range(0, 1):
            # row = fi_payload[i]
            self.openmarket_open_market_table.item(i, 0).setText('Bouwerslaan ' + self.bplr_payload['house_number'] + ' , ' + self.bplr_payload['postal_code'])
            self.openmarket_open_market_table.item(i, 1).setText(str(self.bplr_payload['amount_wanted']))
            self.openmarket_open_market_table.item(i, 2).setText(str(fi_payload['interest_rate']))
            self.openmarket_open_market_table.item(i, 3).setText(str(fi_payload['duration']))

        self.nextScreen()

    def openmarket_view_campaign(self):
        address = 'Bouwerslaan ' + self.bplr_payload['house_number'] + ' , ' + self.bplr_payload['postal_code']
        self.icb_property_address_lineedit.setText(address)
        # self.icb_current_bids_table.setRowCount(0)
        self.nextScreen()

    def icb_place_bid(self):
        # row_count = self.icb_current_bids_table.rowCount()
        # self.icb_current_bids_table.insertRow(row_count)
        # print row_count
        self.icb_current_bids_table.item(0, 0).setText(self.icb_amount_lineedit.text())
        self.icb_current_bids_table.item(0, 1).setText(self.icb_duration_lineedit.text())
        self.icb_current_bids_table.item(0, 2).setText(self.icb_interest_lineedit.text())



#################################################bs#####################################################################

    def setupObjects(self):
        #create user
        self.user_borrower,pub_key1,priv_key1 = self.api.create_user()
        self.user_investor,pub_key2,priv_key2 = self.api.create_user()
        self.user_bank,pub_key3,priv_key3 = self.api.create_user()

        #create profile for users
        # self._basic_forms = {'role': ROLES[1], 'first_name': 'Bob', 'last_name': 'Bauwer, de', 'email': 'bob@gmail.com', 'iban': 'ING 0256 0213', 'phonenumber': '0625457845'}
        # self._borrower_forms = {'current_postalcode': '1234 BA', 'current_housenumber': '123', 'documents_list': []}

        self.borrower_profile_payload = {'role': 1, 'first_name': 'Bob', 'last_name': 'Bouwer, de', 'email': 'bob@gmail.com',
                    'iban': 'NL53 INGBB 04027 30393', 'phonenumber': '+31632549865',
                    'current_postalcode': '1234 CD', 'current_housenumber': '24', 'documents_list': []}
        investor_payload = {'role': 2, 'first_name': 'Ruby', 'last_name': 'Cue', 'email': 'example1@example.com', 'iban': 'NL53 INGB 04097 30394', 'phonenumber': '+3170253719290'}
        bank_payload = {'role': 3}

        print self.api.create_profile(self.user_borrower, self.borrower_profile_payload)
        print self.api.create_profile(self.user_investor, investor_payload)
        print self.api.create_profile(self.user_bank, bank_payload)

    def set_navigation(self):
        self.next_1.clicked.connect(self.nextScreen)
        self.next_2.clicked.connect(self.nextScreen)
        self.next_3.clicked.connect(self.nextScreen)
        self.next_4.clicked.connect(self.nextScreen)
        self.next_5.clicked.connect(self.nextScreen)
        self.next_6.clicked.connect(self.nextScreen)
        self.next_7.clicked.connect(self.nextScreen)
        self.next_8.clicked.connect(self.nextScreen)
        self.prev_1.clicked.connect(self.previousScreen)
        self.prev_2.clicked.connect(self.previousScreen)
        self.prev_3.clicked.connect(self.previousScreen)
        self.prev_4.clicked.connect(self.previousScreen)
        self.prev_5.clicked.connect(self.previousScreen)
        self.prev_6.clicked.connect(self.previousScreen)
        self.prev_7.clicked.connect(self.previousScreen)
        self.prev_8.clicked.connect(self.previousScreen)

    def nextScreen(self):
        self.stackedWidget.setCurrentIndex((self.stackedWidget.currentIndex() + 1) % self.stackedWidget.count())

    def previousScreen(self):
        self.stackedWidget.setCurrentIndex((self.stackedWidget.currentIndex() - 1) % self.stackedWidget.count())



def main():
    app = MarketApplication(sys.argv)
    mainwindow = MainWindowController(app=app)
    mainwindow.show()
    app.exec_()


if __name__ == '__main__':
    main()
