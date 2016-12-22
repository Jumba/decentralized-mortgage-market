from __future__ import absolute_import

import os
import sys
import unittest
from uuid import UUID

from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest

from market.api.api import STATUS
from market.controllers.main_view_controller import MainWindowController
from market.models.role import Role
from market.models.user import User
from market.views.main_view import Ui_MainWindow

from marketGUI.market_app import TestMarketApplication

from mock import Mock, MagicMock


class GUITestSuite(unittest.TestCase):
    def setUp(self):
        self.app = TestMarketApplication(sys.argv)
        self.window = MainWindowController(app=self.app, ui_location=os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../', 'ui/mainwindow.ui'))
        self.window.bplr_controller.banks_ids = [self.window.app.bank1.id, self.window.app.bank2.id,
                                                 self.window.app.bank3.id, self.window.app.bank4.id]

        # Define payloads
        self.payload_loan_request = {'house_id': UUID('b97dfa1c-e125-4ded-9b1a-5066462c520c'), 'mortgage_type': 1,
                                     'banks': self.window.bplr_controller.banks_ids,
                                     'description': unicode('I want to buy a house'), 'amount_wanted': 123456,
                                     'postal_code': '1111AA',
                                     'house_number': '11', 'address': 'straat', 'price': 123456,
                                     'house_link': 'http://www.myhouseee.com/', 'seller_phone_number': '0612345678',
                                     'seller_email': 'seller1@gmail.com'}
        self.payload_mortgage = {'house_id': UUID('b97dfa1c-e125-4ded-9b1a-5066462c520c'), 'mortgage_type': 1,
                                 'amount': 123000, 'interest_rate': 5.5, 'max_invest_rate': 7.0, 'default_rate': 9.0,
                                 'duration': 30, 'risk': 'hi', 'investors': []}
        self.payload_loan_offer = {'role': 1, 'user_key': 'rfghiw98594pio3rjfkhs', 'amount': 1000, 'duration': 24,
                                   'interest_rate': 2.5,
                                   'mortgage_id': UUID('b97dfa1c-e125-4ded-9b1a-5066462c520c'),
                                   'status': STATUS.PENDING}


        # self.app.exec_()

    def tearDown(self):
        # sys.exit()
        pass

    def test_profile_empty(self):
        # Test that the controller calls a QMessageBox with unique input when the form has not been filled in
        self.window.msg.about = MagicMock()
        QTest.mouseClick(self.window.profile_save_pushbutton, Qt.LeftButton)
        self.window.msg.about.assert_called_with(self.window, 'Profile error', 'You didn\'t enter all of the required information.')

    def test_profile_load_current_borrower(self):
        # Testing loading of the current borrower's profile
        self.payload = {'role': 1, 'first_name': u'Bob', 'last_name': u'Saget', 'email': 'example@example.com',
                        'iban': 'NL53 INGBB 04027 30393', 'phonenumber': '+3170253719234',
                        'current_postalcode': '2162CD', 'current_housenumber': '22', 'current_address': 'straat',
                        'documents_list': []}
        self.payload_investor = {'role': 2, 'first_name': u'Ruby', 'last_name': u'Cue', 'email': 'example1@example.com',
                                 'iban': 'NL53 INGB 04097 30393', 'phonenumber': '+3170253719290'}
        pass

    def test_profile_load_current_investor(self):
        # Testing loading of the current investor's profile
        self.payload = {'role': 1, 'first_name': u'Bob', 'last_name': u'Saget', 'email': 'example@example.com',
                        'iban': 'NL53 INGBB 04027 30393', 'phonenumber': '+3170253719234',
                        'current_postalcode': '2162CD', 'current_housenumber': '22', 'current_address': 'straat',
                        'documents_list': []}
        self.payload_investor = {'role': 2, 'first_name': u'Ruby', 'last_name': u'Cue', 'email': 'example1@example.com',
                                 'iban': 'NL53 INGB 04097 30393', 'phonenumber': '+3170253719290'}
        pass

    def test_profile_switch_role_valid(self):
        pass

    def test_profile_switch_role_invalid(self):
        pass

    def test_investors_portfolio_table_empty(self):
        # Create a new investor
        investor, _, _ = self.window.api.create_user()

        # Check if their investments list is empty
        self.assertFalse(self.window.ip_investments_table.rowCount())

    def test_investors_portfolio_table_filled(self):
        # Create the investor user
        role_id = Role.INVESTOR.value
        self.window.app.user.role_id = role_id
        self.window.api.db.put(User.type, self.window.app.user.id, self.window.app.user)

        # Create borrowers
        borrower1, _, _ = self.window.api.create_user()
        role_id = Role.BORROWER.value
        borrower1.role_id = role_id
        self.window.api.db.put(User.type, borrower1.id, borrower1)

        borrower2, _, _ = self.window.api.create_user()
        borrower2.role_id = role_id
        self.window.api.db.put(User.type, borrower2.id, borrower2)

        # Create loan requests
        borrower1 = self.window.api.db.get(User.type, borrower1.id)
        loan_request1 = self.window.api.create_loan_request(borrower1, self.payload_loan_request)

        borrower2 = self.window.api.db.get(User.type, borrower2.id)
        loan_request2 = self.window.api.create_loan_request(borrower2, self.payload_loan_request)

        # Accept the loan requests
        self.payload_mortgage['user_key'] = borrower1.id
        self.payload_mortgage['request_id'] = loan_request1.id
        self.payload_mortgage['house_id'] = self.payload_loan_request['house_id']
        self.payload_mortgage['mortgage_type'] = self.payload_loan_request['mortgage_type']

        accepted_loan_request1, mortgage1 = self.window.api.accept_loan_request(self.window.app.bank1,
                                                                                self.payload_mortgage)

        self.payload_mortgage['user_key'] = borrower2.id
        self.payload_mortgage['request_id'] = loan_request2.id

        accepted_loan_request2, mortgage2 = self.window.api.accept_loan_request(self.window.app.bank1,
                                                                                self.payload_mortgage)

        # Accept mortgages
        self.window.api.accept_mortgage_offer(borrower1, {'mortgage_id' : mortgage1.id})
        self.window.api.accept_mortgage_offer(borrower2, {'mortgage_id' : mortgage2.id})

        # Place loan offers
        self.payload_loan_offer['user_key'] = self.window.app.user.id # set user_key to the investor's public key
        self.payload_loan_offer['mortgage_id'] = mortgage1.id
        loan_offer1 = self.window.api.place_loan_offer(self.window.app.user, self.payload_loan_offer)

        self.payload_loan_offer['mortgage_id'] = mortgage2.id
        self.payload_loan_offer['amount'] = 123456
        loan_offer2 = self.window.api.place_loan_offer(self.window.app.user, self.payload_loan_offer)

        # Accept one of the loan offers
        self.window.api.accept_investment_offer(borrower2, {'investment_id' : loan_offer2.id})

        # Check if the investments are in the table with the right values
        self.window.ip_controller.setup_view()

        # Check first investment
        self.assertEqual(self.window.ip_investments_table.item(0, 0).text(), 'straat 11, 1111AA')
        self.assertEqual(self.window.ip_investments_table.item(0, 1).text(), 'Running')
        self.assertEqual(self.window.ip_investments_table.item(0, 2).text(), 'Pending')
        self.assertEqual(self.window.ip_investments_table.item(0, 3).text(), '1000')
        self.assertEqual(self.window.ip_investments_table.item(0, 4).text(), '2.5')
        self.assertEqual(self.window.ip_investments_table.item(0, 5).text(), '24')

        # Check second investment
        self.assertEqual(self.window.ip_investments_table.item(1, 0).text(), 'straat 11, 1111AA')
        self.assertEqual(self.window.ip_investments_table.item(1, 1).text(), 'Completed')
        self.assertEqual(self.window.ip_investments_table.item(1, 2).text(), 'Accepted')
        self.assertEqual(self.window.ip_investments_table.item(1, 3).text(), '123456')
        self.assertEqual(self.window.ip_investments_table.item(1, 4).text(), '2.5')
        self.assertEqual(self.window.ip_investments_table.item(1, 5).text(), '24')

    def test_banks_portfolio_table_empty(self):
        pass

    def test_banks_portfolio_table_filled(self):
        # TODO Add running and completed campaigns
        pass

    def test_pending_loan_requests_table_empty(self):
        pass

    def test_pending_loan_requests_table_filled(self):
        # TODO Add loan requests for linear and fixed-rate mortgages
        pass

    def test_pending_loan_requests_table_unselected(self):
        pass

    def test_pending_loan_requests_table_selected(self):
        pass

    def test_pending_loan_request_forms_filled(self):
        # TODO Test for linear and fixed-rate mortgages
        pass

    def test_pending_loan_request_accept_empty(self):
        pass

    def test_pending_loan_request_accept_filled_incomplete(self):
        pass

    def test_pending_loan_request_accept_filled_complete(self):
        pass

    def test_pending_loan_request_reject_empty(self):
        pass

    def test_pending_loan_request_reject_filled(self):
        pass


