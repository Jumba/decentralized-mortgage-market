import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from market.views import main_view
from marketGUI.market_app import MarketApplication


class MainWindowController(QStackedWidget, main_view.Ui_StackedWidget):
    def __init__(self, parent=None, app=None):
        super(MainWindowController, self).__init__(parent)
        self.mainwindow = self #to make moving to another class easier
        self.app = app
        self.banks_payload = {}
        self.setupUi(self)
        self.setCurrentIndex(2)
        self.set_navigation()
        self.bplr_submit_button.clicked.connect(self.bplr_submit_loan_request)
        self.fiplr1_loan_requests_table.doubleClicked.connect(self.view_loan_request)


    def view_loan_request(self):
         print self.fiplr1_loan_requests_table.selectedIndexes()[0].row() # index of the row


    def update_table_row(self, row, payload):
        print self.fiplr1_loan_requests_table.item(row, 0).text()
        print payload
        # self.fiplr1_loan_requests_table.item(row, 0).setText(payload['postal_code'])#+' , '+payload['house_number'])
        self.fiplr1_loan_requests_table.item(row, 0).setText(payload['postal_code']+' , '+payload['house_number'])
        self.fiplr1_loan_requests_table.item(row, 1).setText(str(payload['mortgage_type']))
        self.fiplr1_loan_requests_table.item(row, 2).setText(payload['amount_wanted'])
        self.fiplr1_loan_requests_table.item(row, 3).setText(payload['price'])


    def bplr_submit_loan_request(self):
        fields = {'postal_code': self.mainwindow.bplr_postcode_lineedit,
                  'house_number': self.mainwindow.bplr_housenumber_lineedit,
                  'price': self.mainwindow.bplr_house_price_lineedit,
                  'amount_wanted': self.mainwindow.bplr_amount_wanted_lineedit}
        banks = [self.mainwindow.bplr_bank1_checkbox, self.mainwindow.bplr_bank2_checkbox,
                 self.mainwindow.bplr_bank3_checkbox,
                 self.mainwindow.bplr_bank4_checkbox]
        banks_ids = ['1', '2', '3', '4']
        checked_banks = []

        # Get all the inputs
        for key in fields:
            self.banks_payload[key] = fields[key].text()

        #what banks were chosen
        pointer = 0
        for obj in banks:
            if obj.checkState():
                checked_banks += banks_ids[pointer]
            pointer += 1
        self.banks_payload['banks'] = checked_banks

        #check the chosen mortgage type
        if self.mainwindow.bplr_linear_radiobutton.isChecked():
            self.banks_payload['mortgage_type'] = 0
        else:
            self.banks_payload['mortgage_type'] = 1

        self.banks_payload['description'] = self.mainwindow.bplr_description_textedit.toPlainText(),

        self.setCurrentIndex(4)
        self.update_table_row(0, self.banks_payload)

    def set_navigation(self):
        self.next_1.clicked.connect(self.next_screen)
        self.next_2.clicked.connect(self.next_screen)
        self.next_3.clicked.connect(self.next_screen)
        self.next_4.clicked.connect(self.next_screen)
        self.next_5.clicked.connect(self.next_screen)
        self.next_6.clicked.connect(self.next_screen)
        self.next_7.clicked.connect(self.next_screen)
        self.next_8.clicked.connect(self.next_screen)
        self.prev_1.clicked.connect(self.prev_screen)
        self.prev_2.clicked.connect(self.prev_screen)
        self.prev_3.clicked.connect(self.prev_screen)
        self.prev_4.clicked.connect(self.prev_screen)
        self.prev_5.clicked.connect(self.prev_screen)
        self.prev_6.clicked.connect(self.prev_screen)
        self.prev_7.clicked.connect(self.prev_screen)
        self.prev_8.clicked.connect(self.prev_screen)

    def next_screen(self):
        self.setCurrentIndex((self.currentIndex() + 1) % 8)

    def prev_screen(self):
        self.setCurrentIndex((self.currentIndex() - 1) % 8)


def main():
    app = MarketApplication(sys.argv)
    mainwindow = MainWindowController(app=app)
    mainwindow.show()
    app.exec_()


if __name__ == '__main__':
    main()
