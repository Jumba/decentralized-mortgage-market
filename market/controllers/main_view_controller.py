import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from market.views import main_view
from marketGUI.market_app import MarketApplication
# from place_loan_request_controller import PlaceLoanRequestController
import place_loan_request_controller


class MainWindowController(QStackedWidget, main_view.Ui_StackedWidget):
    def __init__(self, parent=None, app=None):
        super(MainWindowController, self).__init__(parent)
        self.mainwindow = self #to make moving to another class easier
        self.app = app
        self.setupUi(self)
        self.setCurrentIndex(2)
        self.setNavigation()
        self.bplr_submit_button.clicked.connect(self.bplr_submit_loan_request)

    def bplr_submit_loan_request(self):
        fields = {'postal_code': self.mainwindow.bplr_postcode_lineedit,
                  'house_number': self.mainwindow.bplr_housenumber_lineedit,
                  'price': self.mainwindow.bplr_house_price_lineedit,
                  'description': self.mainwindow.bplr_description_textedit,
                  'amount_wanted': self.mainwindow.bplr_amount_wanted_lineedit}
        banks = [self.mainwindow.bplr_bank1_checkbox, self.mainwindow.bplr_bank2_checkbox,
                 self.mainwindow.bplr_bank3_checkbox,
                 self.mainwindow.bplr_bank4_checkbox]
        banks_ids = ['1', '2', '3', '4']
        banks_payload = []

        #what banks were chosen
        pointer = 0
        for obj in banks:
            if obj.checkState():
                banks_payload += banks_ids[pointer]
            pointer += 1
        fields['banks'] = banks_payload

        #check the chosen mortgage type
        if self.mainwindow.bplr_linear_radiobutton.isChecked():
            fields['mortgage_type'] = 0
        else:
            fields['mortgage_type'] = 1
        self.payload = fields
        self.setCurrentIndex(4)

    def setNavigation(self):
        self.next_1.clicked.connect(self.nextScreen)
        self.next_2.clicked.connect(self.nextScreen)
        self.next_3.clicked.connect(self.nextScreen)
        self.next_4.clicked.connect(self.nextScreen)
        self.next_5.clicked.connect(self.nextScreen)
        self.next_6.clicked.connect(self.nextScreen)
        self.next_7.clicked.connect(self.nextScreen)
        self.next_8.clicked.connect(self.nextScreen)
        self.prev_1.clicked.connect(self.prevScreen)
        self.prev_2.clicked.connect(self.prevScreen)
        self.prev_3.clicked.connect(self.prevScreen)
        self.prev_4.clicked.connect(self.prevScreen)
        self.prev_5.clicked.connect(self.prevScreen)
        self.prev_6.clicked.connect(self.prevScreen)
        self.prev_7.clicked.connect(self.prevScreen)
        self.prev_8.clicked.connect(self.prevScreen)

    def nextScreen(self):
        self.setCurrentIndex((self.currentIndex() + 1) % 8)

    def prevScreen(self):
        self.setCurrentIndex((self.currentIndex() - 1) % 8)


def main():
    app = MarketApplication(sys.argv)
    mainwindow = MainWindowController(app=app)
    mainwindow.show()
    app.exec_()


if __name__ == '__main__':
    main()
