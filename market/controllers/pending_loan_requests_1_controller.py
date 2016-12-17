from PyQt5 import QtWidgets


class PendingLoanRequests1Controller:
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow

    def setup_view(self):
        loan_request_table = self.mainwindow.fiplr1_loan_requests_table

        # Getting the loan requests for the bank
        loan_requests = self.mainwindow.api.load_all_loan_requests(self.mainwindow.app.user)

        # If the list is empty, do nothing. Otherwise fill table
        if loan_requests:
            # Fill the mortgage table
            for [loan_request, house] in loan_requests:
                # Property Address, Campaign Status, Investment Status, Amount Invested, Interest, Duration
                address = house.postal_code + ', ' + house.house_number

                mortgage_type = ''
                if loan_request.mortgage_type == 1:
                    mortgage_type = 'Linear'
                elif loan_request.mortgage_type == 2:
                    mortgage_type = 'Fixed-Rate'

                row_count = loan_request_table.rowCount()
                loan_request_table.insertRow(row_count)
                loan_request_table.setItem(row_count, 0, QtWidgets.QTableWidgetItem(address))
                loan_request_table.setItem(row_count, 0, QtWidgets.QTableWidgetItem(mortgage_type))
                loan_request_table.setItem(row_count, 0, QtWidgets.QTableWidgetItem(str(loan_request.amount_wanted)))
                loan_request_table.setItem(row_count, 0, QtWidgets.QTableWidgetItem(str(house.price)))


