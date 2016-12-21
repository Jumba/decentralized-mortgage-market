from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox


class PendingLoanRequests1Controller:
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.loan_request_table = self.mainwindow.fiplr1_loan_requests_table
        self.loan_requests = []

        # Add listener to the 'view loan request' button
        self.mainwindow.fiplr1_view_loan_request_pushbutton.clicked.connect(self.show_request)

    def setup_view(self):
        # Clear table
        self.loan_request_table.setRowCount(0)

        # Getting the loan requests for the bank
        self.loan_requests = self.mainwindow.api.load_all_loan_requests(self.mainwindow.app.user)

        # If the list is empty, do nothing. Otherwise fill table
        if self.loan_requests:
            # Fill the mortgage table
            for [loan_request, house] in self.loan_requests:
                # Property Address, Campaign Status, Investment Status, Amount Invested, Interest, Duration
                address = house.address + ' ' + house.house_number + ', ' + house.postal_code

                mortgage_type = ''
                if loan_request.mortgage_type == 1:
                    mortgage_type = 'Linear'
                elif loan_request.mortgage_type == 2:
                    mortgage_type = 'Fixed-Rate'

                row_count = self.loan_request_table.rowCount()
                self.loan_request_table.insertRow(row_count)
                self.loan_request_table.setItem(row_count, 0, QtWidgets.QTableWidgetItem(address))
                self.loan_request_table.setItem(row_count, 1, QtWidgets.QTableWidgetItem(mortgage_type))
                self.loan_request_table.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str(
                    loan_request.amount_wanted)))
                self.loan_request_table.setItem(row_count, 3, QtWidgets.QTableWidgetItem(str(house.price)))

    def show_request(self):
        try:
            # Get the selected row index
            selected_index = self.loan_request_table.selectedIndexes()[0].row()
            # If a request has been selected, show it
            [loan_request, _] = self.loan_requests[selected_index]
            self.mainwindow.fiplr2_controller.setup_view(loan_request.id)
            self.mainwindow.navigation.switch_to_fiplr2()
        except IndexError:
            self.mainwindow.show_dialog("Select request", 'No loan requests have been selected.')
