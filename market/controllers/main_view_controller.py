import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from market.database.backends import MemoryBackend
from market.database.database import MockDatabase
from market.views import main_view
from marketGUI.market_app import MarketApplication
from market.api.api import MarketAPI


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
        self.setupObjects()

        self.stackedWidget.setCurrentIndex(0)
        print self.stackedWidget.count()

    def fiplr2_view_loan_request(self):
        chosen_index = self.fiplr1_loan_requests_table.selectedIndexes()[0].row();
        request = self.bplr_payload[chosen_index]     # index of the row
        #personal information
        #information about the request
        self.fiplr2_property_address_lineedit.text('Bouwerslaan '+request['house_number']+' , '+request['postal_code'])
        # self.fiplr2_property_address_lineedit

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
        self.loadAllPendingLoanRequests()

    def loadAllPendingLoanRequests(self):
        pop = self.api.load_all_loan_requests(self.user_bank)
        print pop
        self.fiplr1_populate_table(pop)

    # method for populating the pending resquest table.
    def fiplr1_populate_table(self, payload):
        self.fiplr1_loan_requests_table.setRowCount(len(payload))
        for i in range(0, len(payload)):
            row = payload[i]
            # print row
            val = row['house_number']+' , '+row['postal_code']
            self.fiplr1_loan_requests_table.item(i, 0).setText(val)
            self.fiplr1_loan_requests_table.item(i, 1).setText(str(row['mortgage_type']))
            self.fiplr1_loan_requests_table.item(i, 2).setText(row['amount_wanted'])
            self.fiplr1_loan_requests_table.item(i, 3).setText(row['price'])



    def setupObjects(self):
        #create user
        self.user_borrower,pub_key1,priv_key1 = self.api.create_user()
        self.user_investor,pub_key2,priv_key2 = self.api.create_user()
        self.user_bank,pub_key3,priv_key3 = self.api.create_user()

        #create profile for users
        # self._basic_forms = {'role': ROLES[1], 'first_name': 'Bob', 'last_name': 'Bauwer, de', 'email': 'bob@gmail.com', 'iban': 'ING 0256 0213', 'phonenumber': '0625457845'}
        # self._borrower_forms = {'current_postalcode': '1234 BA', 'current_housenumber': '123', 'documents_list': []}

        borrower_payload = {'role': 1, 'first_name': 'Bob', 'last_name': 'Bouwer, de', 'email': 'bob@gmail.com',
                    'iban': 'NL53 INGBB 04027 30393', 'phonenumber': '+31632549865',
                    'current_postalcode': '1234 CD', 'current_housenumber': '24', 'documents_list': []}
        investor_payload = {'role': 2, 'first_name': 'Ruby', 'last_name': 'Cue', 'email': 'example1@example.com', 'iban': 'NL53 INGB 04097 30394', 'phonenumber': '+3170253719290'}
        bank_payload = {'role': 3}

        print self.api.create_profile(self.user_borrower, borrower_payload)
        print self.api.create_profile(self.user_investor, investor_payload)
        print self.api.create_profile(self.user_bank, bank_payload)

    def set_navigation(self):
        self.next_1.clicked.connect(self.next_screen)
        self.next_2.clicked.connect(self.next_screen)
        self.next_3.clicked.connect(self.next_screen)
        self.next_4.clicked.connect(self.next_screen)
        self.next_5.clicked.connect(self.next_screen)
        self.next_6.clicked.connect(self.next_screen)
        # self.next_7.clicked.connect(self.next_screen)
        # self.next_8.clicked.connect(self.next_screen)
        self.prev_1.clicked.connect(self.prev_screen)
        self.prev_2.clicked.connect(self.prev_screen)
        self.prev_3.clicked.connect(self.prev_screen)
        self.prev_4.clicked.connect(self.prev_screen)
        self.prev_5.clicked.connect(self.prev_screen)
        self.prev_6.clicked.connect(self.prev_screen)
        # self.prev_7.clicked.connect(self.prev_screen)
        # self.prev_8.clicked.connect(self.prev_screen)

    def next_screen(self):
        self.stackedWidget.setCurrentIndex((self.stackedWidget.currentIndex() + 1) % self.stackedWidget.count())

    def prev_screen(self):
        self.stackedWidget.setCurrentIndex((self.stackedWidget.currentIndex() - 1) % self.stackedWidget.count())



def main():
    app = MarketApplication(sys.argv)
    mainwindow = MainWindowController(app=app)
    mainwindow.show()
    app.exec_()


if __name__ == '__main__':
    main()
