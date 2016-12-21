from __future__ import absolute_import

import os
import sys
import unittest
from uuid import UUID

from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest

from market.controllers.main_view_controller import MainWindowController
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

        # self.app.exec_()

    def tearDown(self):
        # sys.exit()
        pass


    def test_profile_empty(self):
        # Test that the controller calls a QMessageBox with unique input when the form has not been filled in
        self.window.msg.about = MagicMock()
        QTest.mouseClick(self.window.profile_save_pushbutton, Qt.LeftButton)
        self.window.msg.about.assert_called_with(self.window, 'Profile error', 'You didn\'t enter all of the required information.')

    def test_profile_create_profile(self):
        # Testing loading of the current borrower's profile
        payload = {'role': 1, 'first_name': u'Bob', 'last_name': u'Saget', 'email': 'example@example.com',
                        'iban': 'NL53 INGBB 04027 30393', 'phonenumber': '+3170253719234',
                        'current_postalcode': '2162CD', 'current_housenumber': '22', 'current_address': 'straat',
                        'documents_list': []}
        self.assertEqual(None, self.window.profile_controller.current_profile)

        # Create profile so when we can populate the form easier
        user, _, _ = self.app.api.create_user()
        profile = self.app.api.create_profile(user, payload)
        self.assertNotEqual(None, profile)

        # Fill in the form and press the 'save'-button
        self.window.profile_controller.update_form(profile)
        self.window.msg.about = MagicMock()
        QTest.mouseClick(self.window.profile_save_pushbutton, Qt.LeftButton)
        self.window.msg.about.assert_called_with(self.window, 'Profile saved', 'Your profile has been saved.')

    def test_profile_load_current_borrower(self):
        # Testing loading of the current borrower's profile
        payload = {'role': 1, 'first_name': u'Bob', 'last_name': u'Saget', 'email': 'example@example.com',
                        'iban': 'NL53 INGBB 04027 30393', 'phonenumber': '+3170253719234',
                        'current_postalcode': '2162CD', 'current_housenumber': '22', 'current_address': 'straat',
                        'documents_list': []}
        self.assertEqual(None, self.window.profile_controller.current_profile)
        profile = self.app.api.create_profile(self.app.user, payload)
        self.assertNotEqual(None, profile)
        self.window.profile_controller.setup_view()
        # Check if the input fields are the same as the payload
        self.assertEqual(self.window.profile_firstname_lineedit.text(), 'Bob')
        self.assertEqual(self.window.profile_lastname_lineedit.text(), 'Saget')
        self.assertEqual(self.window.profile_email_lineedit.text(), 'example@example.com')
        self.assertEqual(self.window.profile_iban_lineedit.text(), 'NL53 INGBB 04027 30393')
        self.assertEqual(self.window.profile_phonenumber_lineedit.text(), '+3170253719234')
        self.assertEqual(self.window.profile_postcode_lineedit.text(), '2162CD')
        self.assertEqual(self.window.profile_housenumber_lineedit.text(), '22')
        self.assertEqual(self.window.profile_address_lineedit.text(), 'straat')

    def test_profile_load_current_investor(self):
        payload_investor = {'role': 2, 'first_name': u'Ruby', 'last_name': u'Cue', 'email': 'example1@example.com',
                                 'iban': 'NL53 INGBB 04027 30393', 'phonenumber': '+3170253719290'}
        profile = self.app.api.create_profile(self.app.user, payload_investor)
        self.assertNotEqual(None, profile)
        self.window.profile_controller.setup_view()
        # Check if the input fields are the same as the payload
        self.assertEqual(self.window.profile_firstname_lineedit.text(), 'Ruby')
        self.assertEqual(self.window.profile_lastname_lineedit.text(), 'Cue')
        self.assertEqual(self.window.profile_email_lineedit.text(), 'example1@example.com')
        self.assertEqual(self.window.profile_iban_lineedit.text(), 'NL53 INGBB 04027 30393')
        self.assertEqual(self.window.profile_phonenumber_lineedit.text(), '+3170253719290')

    def test_profile_switch_role_valid(self):
        # A user is only allowed to switch roles when he has no active loan requests or campaigns
        payload = {'role': 1, 'first_name': u'Bob', 'last_name': u'Saget', 'email': 'example@example.com',
                   'iban': 'NL53 INGBB 04027 30393', 'phonenumber': '+3170253719234',
                   'current_postalcode': '2162CD', 'current_housenumber': '22', 'current_address': 'straat',
                   'documents_list': []}
        payload_investor = {'role': 2, 'first_name': u'Ruby', 'last_name': u'Cue', 'email': 'example1@example.com',
                            'iban': 'NL53 INGBB 04027 30393', 'phonenumber': '+3170253719290'}
        profile = self.app.api.create_profile(self.app.user, payload)
        self.assertNotEqual(None, profile)
        # self.window.profile_controller.setup_view()

        # Try to switch from borrower to investor
        user, _, _ = self.app.api.create_user()
        new_profile = self.app.api.create_profile(user, payload_investor)
        self.app.user.role_id = 2
        self.window.profile_controller.update_form(new_profile)

        self.window.msg.about = MagicMock()
        QTest.mouseClick(self.window.profile_save_pushbutton, Qt.LeftButton)
        self.window.msg.about.assert_called_with(self.window, 'Profile saved', 'Your profile has been saved.')

    def test_profile_switch_role_invalid(self):
        # A user is only allowed to switch roles when he has no active loan requests or campaigns
        payload = {'role': 1, 'first_name': u'Bob', 'last_name': u'Saget', 'email': 'example@example.com',
                   'iban': 'NL53 INGBB 04027 30393', 'phonenumber': '+3170253719234',
                   'current_postalcode': '2162CD', 'current_housenumber': '22', 'current_address': 'straat',
                   'documents_list': []}
        payload_investor = {'role': 2, 'first_name': u'Ruby', 'last_name': u'Cue', 'email': 'example1@example.com',
                            'iban': 'NL53 INGBB 04027 30393', 'phonenumber': '+3170253719290'}
        payload_loan_request = {'house_id': UUID('b97dfa1c-e125-4ded-9b1a-5066462c520c') , 'mortgage_type': 1, 'banks': [],
                                     'description': unicode('I want to buy a house'), 'amount_wanted': 123456, 'postal_code' : '1111AA', 'house_number' : '11', 'address' : 'straat', 'price' : 123456,
                                     'house_link': 'http://www.myhouseee.com/', 'seller_phone_number': '0612345678',
                                     'seller_email': 'seller1@gmail.com'}
        profile = self.app.api.create_profile(self.app.user, payload)
        self.assertNotEqual(None, profile)
        # self.window.profile_controller.setup_view()

        # Place a loan request
        self.app.api.create_loan_request(self.app.user, payload_loan_request)
        # Try to switch from borrower to investor
        user, _, _ = self.app.api.create_user()
        new_profile = self.app.api.create_profile(user, payload_investor)
        self.app.user.role_id = 2
        self.window.profile_controller.update_form(new_profile)

        self.window.msg.about = MagicMock()
        QTest.mouseClick(self.window.profile_save_pushbutton, Qt.LeftButton)
        self.window.msg.about.assert_called_with(self.window, 'Role switch failed',
                                                 'It is not possible to change your role at this time')

    def test_investors_portfolio_table_empty(self):
        pass

    def test_investors_portfolio_table_filled(self):
        # TODO Add accepted and pending investments with running and completed campaigns
        pass

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


