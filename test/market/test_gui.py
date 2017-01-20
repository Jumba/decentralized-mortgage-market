from __future__ import absolute_import

import os
import sys
import unittest
from uuid import UUID

from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest

from market.api.api import STATUS
from market.controllers.main_window_controller import MainWindowController, QTableWidget
from market.controllers.navigation import NavigateUser
from market.controllers.openmarket_controller import OpenMarketController
from market.models.role import Role
from market.models.user import User

from marketGUI.market_app import TestMarketApplication

from mock import MagicMock


class GUITestSuite(unittest.TestCase):
    def setUp(self):
        self.app = TestMarketApplication(sys.argv)
        self.window = MainWindowController(app=self.app,
                                           ui_location=os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                                    '../../', 'ui/mainwindow.ui'))

        # Clear the database
        self.app.api.db.backend.clear()

        # Create new users
        user, _, _ = self.app.api.create_user()
        bank_role = Role.FINANCIAL_INSTITUTION.value
        bank1, _, _ = self.app.api.create_user()
        bank2, _, _ = self.app.api.create_user()
        bank3, _, _ = self.app.api.create_user()
        bank4, _, _ = self.app.api.create_user()
        bank1.role_id = bank_role
        bank2.role_id = bank_role
        bank3.role_id = bank_role
        bank4.role_id = bank_role
        self.app.api.db.put(User.type, bank1.id, bank1)
        self.app.api.db.put(User.type, bank2.id, bank2)
        self.app.api.db.put(User.type, bank3.id, bank3)
        self.app.api.db.put(User.type, bank4.id, bank4)
        self.app.user = user
        self.app.bank1 = bank1
        self.app.bank2 = bank2
        self.app.bank3 = bank3
        self.app.bank4 = bank4
        self.window.bplr_controller.banks_ids = [self.app.bank1.id, self.app.bank2.id, self.app.bank3.id,
                                                 self.app.bank4.id]

        # Define payloads
        self.payload_borrower_profile = {'role': 1, 'first_name': u'Bob', 'last_name': u'Saget',
                                         'email': 'example@example.com', 'iban': 'NL53 INGBB 04027 30393',
                                         'phonenumber': '+3170253719234', 'current_postalcode': '2162CD',
                                         'current_housenumber': '22', 'current_address': 'straat',
                                         'documents_list': []}
        self.payload_investor_profile = {'role': 2, 'first_name': u'Ruby', 'last_name': u'Cue',
                                         'email': 'example1@example.com', 'iban': 'NL53 INGBB 04027 30393',
                                         'phonenumber': '+3170253719290'}
        self.payload_loan_request = {'house_id': UUID('b97dfa1c-e125-4ded-9b1a-5066462c520c'), 'mortgage_type': 1,
                                     'banks': [self.app.bank1.id, self.app.bank2.id, self.app.bank3.id,
                                               self.app.bank4.id], 'description': unicode('I want to buy a house'),
                                     'amount_wanted': 123456, 'postal_code': '1111AA',
                                     'house_number': '11', 'address': 'straat', 'price': 123456,
                                     'house_link': 'http://www.myhouseee.com/', 'seller_phone_number': '0612345678',
                                     'seller_email': 'seller1@gmail.com'}
        self.payload_mortgage = {'house_id': UUID('b97dfa1c-e125-4ded-9b1a-5066462c520c'), 'mortgage_type': 1,
                                 'amount': 123000, 'interest_rate': 5.5, 'max_invest_rate': 7.0,
                                 'default_rate': 9.0, 'duration': 30, 'risk': 'hi', 'investors': []}
        self.payload_loan_offer = {'role': 1, 'user_key': 'rfghiw98594pio3rjfkhs', 'amount': 1000, 'duration': 24,
                                   'interest_rate': 2.5, 'mortgage_id': UUID('b97dfa1c-e125-4ded-9b1a-5066462c520c'),
                                   'status': STATUS.PENDING}

    def test_profile_empty(self):
        """
        This test checks if a dialog pops up when the 'save profile' button has been clicked without
        filling in all the required information
        """
        self.window.msg.about = MagicMock()
        QTest.mouseClick(self.window.profile_save_pushbutton, Qt.LeftButton)
        self.window.msg.about.assert_called_with(self.window, 'Profile error',
                                                 'You didn\'t enter all of the required information.')

    def test_profile_create_profile(self):
        """
        This test checks if a dialog pops up when the 'save profile' button in the 'profile' screen
        has been clicked after filling in all the required information
        """
        # Test if the user doesn't have a profile yet
        self.window.profile_controller.setup_view()
        self.assertEqual(None, self.window.profile_controller.current_profile)

        # Create a profile
        user, _, _ = self.app.api.create_user()
        profile = self.app.api.create_profile(user, self.payload_borrower_profile)
        self.assertNotEqual(None, profile)

        # Fill in the form and press the 'save' button
        self.window.profile_controller.update_form(profile)
        self.window.msg.about = MagicMock()
        QTest.mouseClick(self.window.profile_save_pushbutton, Qt.LeftButton)
        self.window.msg.about.assert_called_with(self.window, 'Profile saved', 'Your profile has been saved.')

    def test_profile_load_current_borrower(self):
        """
        This test checks the loading of an existing borrower's profile into the 'profile' screen
        """
        # Check if there is no profile on start up
        self.window.profile_controller.setup_view()
        self.assertEqual(None, self.window.profile_controller.current_profile)

        # Create a profile
        profile = self.app.api.create_profile(self.app.user, self.payload_borrower_profile)
        self.assertNotEqual(None, profile)

        # Check if the input fields are the same as the saved profile
        self.window.profile_controller.setup_view()
        self.assertEqual(self.window.profile_firstname_lineedit.text(), 'Bob')
        self.assertEqual(self.window.profile_lastname_lineedit.text(), 'Saget')
        self.assertEqual(self.window.profile_email_lineedit.text(), 'example@example.com')
        self.assertEqual(self.window.profile_iban_lineedit.text(), 'NL53 INGBB 04027 30393')
        self.assertEqual(self.window.profile_phonenumber_lineedit.text(), '+3170253719234')
        self.assertEqual(self.window.profile_postcode_lineedit.text(), '2162CD')
        self.assertEqual(self.window.profile_housenumber_lineedit.text(), '22')
        self.assertEqual(self.window.profile_address_lineedit.text(), 'straat')

    def test_profile_load_current_investor(self):
        """
        This test checks the loading of an existing investor's profile into the 'profile' screen
        """
        # Check if there is no current profile on start up
        self.assertEqual(None, self.window.profile_controller.current_profile)

        # Create profile
        profile = self.app.api.create_profile(self.app.user, self.payload_investor_profile)
        self.assertNotEqual(None, profile)

        # Check if the input fields are the same as the saved profile
        self.window.profile_controller.setup_view()
        self.assertEqual(self.window.profile_firstname_lineedit.text(), 'Ruby')
        self.assertEqual(self.window.profile_lastname_lineedit.text(), 'Cue')
        self.assertEqual(self.window.profile_email_lineedit.text(), 'example1@example.com')
        self.assertEqual(self.window.profile_iban_lineedit.text(), 'NL53 INGBB 04027 30393')
        self.assertEqual(self.window.profile_phonenumber_lineedit.text(), '+3170253719290')

    def test_profile_switch_role_valid(self):
        """
        This test checks a valid role switch in the 'profile' screen. A user is only allowed
        to switch roles when they have no active loan requests or campaigns
        """
        # Create a borrower's profile
        profile = self.app.api.create_profile(self.app.user, self.payload_borrower_profile)
        self.assertNotEqual(None, profile)

        # Load the profile
        self.window.profile_controller.setup_view()

        # Try to switch from borrower to investor
        self.window.profile_investor_radiobutton.setChecked(True)

        # Check if the role has been switched
        self.window.msg.about = MagicMock()
        QTest.mouseClick(self.window.profile_save_pushbutton, Qt.LeftButton)
        self.window.msg.about.assert_called_with(self.window, 'Profile saved', 'Your profile has been saved.')

        # Try to switch back from investor to borrower
        self.window.profile_borrower_radiobutton.setChecked(True)

        # Check if the role has been switched
        self.window.msg.about = MagicMock()
        QTest.mouseClick(self.window.profile_save_pushbutton, Qt.LeftButton)
        self.window.msg.about.assert_called_with(self.window, 'Profile saved', 'Your profile has been saved.')

    def test_profile_switch_role_invalid(self):
        """
        This test checks an invalid role switch in the profile screen. A user is only allowed
        to switch roles when they have no active loan requests or campaigns
        """
        # A user is only allowed to switch roles when he has no active loan requests or campaigns
        profile = self.app.api.create_profile(self.app.user, self.payload_borrower_profile)
        self.assertNotEqual(None, profile)
        # self.window.profile_controller.setup_view()

        # Place a loan request
        self.app.api.create_loan_request(self.app.user, self.payload_loan_request)

        # Load the borrower user's profile
        self.window.profile_controller.setup_view()

        # Try to switch from borrower to investor
        self.window.profile_investor_radiobutton.setChecked(True)

        # Check if the role hasn't been switched
        self.window.msg.about = MagicMock()
        QTest.mouseClick(self.window.profile_save_pushbutton, Qt.LeftButton)
        self.window.msg.about.assert_called_with(self.window, 'Role switch failed',
                                                 'It is not possible to change your role at this time')

    def test_place_loan_request_empty(self):
        """
        This test checks if a dialog pops up if the 'submit' button in the 'place loan request'
        screen has been clicked without entering any information
        """
        self.app.api.create_profile(self.app.user, self.payload_borrower_profile)

        self.window.msg.about = MagicMock()
        QTest.mouseClick(self.window.bplr_submit_pushbutton, Qt.LeftButton)
        self.window.msg.about.assert_called_with(self.window, 'Loan request error',
                                                 "You didn't enter the required information.")

    def test_place_loan_request_filled_in_linear(self):
        """
        This test checks if a dialog pops up when the 'submit' button in the 'place loan request'
        screen has been clicked after entering all information
        """
        self.app.api.create_profile(self.app.user, self.payload_borrower_profile)
        self.window.bplr_address_lineedit.setText('straat')
        self.window.bplr_postcode_lineedit.setText('1111aa')
        self.window.bplr_housenumber_lineedit.setText('123')
        self.window.bplr_house_price_lineedit.setText('90')
        self.window.bplr_amount_wanted_lineedit.setText('100')
        self.window.bplr_description_textedit.setText('description')
        self.window.bplr_seller_phone_number_lineedit.setText('0614575412')
        self.window.bplr_seller_email_lineedit.setText('example@example.com')
        self.window.bplr_house_link_lineedit.setText('link.com/link')
        self.window.bplr_bank1_checkbox.setChecked(True)

        self.window.msg.about = MagicMock()
        QTest.mouseClick(self.window.bplr_submit_pushbutton, Qt.LeftButton)
        self.window.msg.about.assert_called_with(self.window, "Loan request created",
                                                 'Your loan request has been sent.')

    def test_place_loan_request_filled_in_fixedrate(self):
        """
        This test checks if a dialog pops up when the 'submit' button in the 'place loan request'
        screen has been clicked after entering all information
        """
        self.app.api.create_profile(self.app.user, self.payload_borrower_profile)
        self.window.bplr_address_lineedit.setText('straat')
        self.window.bplr_postcode_lineedit.setText('1111aa')
        self.window.bplr_housenumber_lineedit.setText('123')
        self.window.bplr_house_price_lineedit.setText('90')
        self.window.bplr_amount_wanted_lineedit.setText('100')
        self.window.bplr_description_textedit.setText('description')
        self.window.bplr_seller_phone_number_lineedit.setText('0614575412')
        self.window.bplr_seller_email_lineedit.setText('example@example.com')
        self.window.bplr_house_link_lineedit.setText('link.com/link')
        self.window.bplr_bank1_checkbox.setChecked(True)
        self.window.bplr_fixedrate_radiobutton.setChecked(True)

        self.window.msg.about = MagicMock()
        QTest.mouseClick(self.window.bplr_submit_pushbutton, Qt.LeftButton)
        self.window.msg.about.assert_called_with(self.window, "Loan request created",
                                                 'Your loan request has been sent.')

    def test_place_loan_request_no_banks(self):
        """
        This test checks if a dialog pops up if the 'submit' button in the 'place loan request'
        screen has been clicked without selecting any banks
        """
        self.app.api.create_profile(self.app.user, self.payload_borrower_profile)
        self.window.bplr_address_lineedit.setText('straat')
        self.window.bplr_postcode_lineedit.setText('1111aa')
        self.window.bplr_housenumber_lineedit.setText('123')
        self.window.bplr_house_price_lineedit.setText('90')
        self.window.bplr_amount_wanted_lineedit.setText('100')
        self.window.bplr_description_textedit.setText('description')
        self.window.bplr_seller_phone_number_lineedit.setText('0614575412')
        self.window.bplr_seller_email_lineedit.setText('example@example.com')
        self.window.bplr_house_link_lineedit.setText('link.com/link')

        self.window.msg.about = MagicMock()
        QTest.mouseClick(self.window.bplr_submit_pushbutton, Qt.LeftButton)
        self.window.msg.about.assert_called_with(self.window, 'Loan request error',
                                                 "You didn't enter the required information.")

    def test_place_loan_request_filled_in_twice(self):
        """
        This test checks if a dialog pops up if the 'submit' button in the 'place loan request'
        screen has been clicked twice. The user can only have one loan request at a time
        """
        self.app.api.create_profile(self.app.user, self.payload_borrower_profile)
        self.window.bplr_address_lineedit.setText('straat')
        self.window.bplr_postcode_lineedit.setText('1111aa')
        self.window.bplr_housenumber_lineedit.setText('123')
        self.window.bplr_house_price_lineedit.setText('90')
        self.window.bplr_amount_wanted_lineedit.setText('100')
        self.window.bplr_description_textedit.setText('description')
        self.window.bplr_seller_phone_number_lineedit.setText('0614575412')
        self.window.bplr_seller_email_lineedit.setText('example@example.com')
        self.window.bplr_house_link_lineedit.setText('link.com/link')
        self.window.bplr_bank1_checkbox.setChecked(True)

        self.window.msg.about = MagicMock()
        QTest.mouseClick(self.window.bplr_submit_pushbutton, Qt.LeftButton)
        QTest.mouseClick(self.window.bplr_submit_pushbutton, Qt.LeftButton)
        self.window.msg.about.assert_called_with(self.window, 'Loan request error',
                                                 'You can only have a single loan request.')

    def create_mortgage_campaign_and_bids(self):
        """
        This function creates two loan requests, both with a mortgage and a loan offer
        """
        role_id = Role.INVESTOR.value
        self.window.app.user.role_id = role_id
        self.window.api.create_profile(self.window.app.user, self.payload_investor_profile)
        self.window.api.db.put(User.type, self.window.app.user.id, self.window.app.user)

        # Create borrowers
        borrower1, _, _ = self.window.api.create_user()
        role_id = Role.BORROWER.value
        borrower1.role_id = role_id
        self.window.api.create_profile(borrower1, self.payload_borrower_profile)
        self.window.api.db.put(User.type, borrower1.id, borrower1)

        borrower2, _, _ = self.window.api.create_user()
        borrower2.role_id = role_id
        self.window.api.create_profile(borrower2, self.payload_borrower_profile)
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
        self.window.api.accept_mortgage_offer(borrower1, {'mortgage_id': mortgage1.id})
        self.window.api.accept_mortgage_offer(borrower2, {'mortgage_id': mortgage2.id})

        # Place loan offers
        self.payload_loan_offer['user_key'] = self.window.app.user.id  # set user_key to the investor's public key
        self.payload_loan_offer['mortgage_id'] = mortgage1.id
        self.window.api.place_loan_offer(self.window.app.user, self.payload_loan_offer)

        self.payload_loan_offer['mortgage_id'] = mortgage2.id
        self.payload_loan_offer['amount'] = 123456
        loan_offer2 = self.window.api.place_loan_offer(self.window.app.user, self.payload_loan_offer)

        # Accept one of the loan offers
        self.window.api.accept_investment_offer(borrower2, {'investment_id': loan_offer2.id})

    def test_openmarket_table_empty(self):
        """
        This test checks if the table in the 'open market' screen is empty when there are no campaigns
        """
        self.window.openmarket_controller.setup_view()
        self.assertFalse(self.window.openmarket_open_market_table.rowCount())

    def test_openmarket_table_filled(self):
        """
        This test checks if the table in the 'open market' screen is not empty when there are campaigns
        """
        # Create the investor user
        role_id = Role.INVESTOR.value
        self.window.app.user.role_id = role_id
        self.window.api.db.put(User.type, self.window.app.user.id, self.window.app.user)

        # Create borrowers
        borrower1, _, _ = self.window.api.create_user()
        role_id = Role.BORROWER.value
        borrower1.role_id = role_id
        self.window.api.create_profile(borrower1, self.payload_borrower_profile)
        self.window.api.db.put(User.type, borrower1.id, borrower1)

        borrower2, _, _ = self.window.api.create_user()
        borrower2.role_id = role_id
        self.window.api.create_profile(borrower2, self.payload_borrower_profile)
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
        self.window.api.accept_mortgage_offer(borrower1, {'mortgage_id': mortgage1.id})
        self.window.api.accept_mortgage_offer(borrower2, {'mortgage_id': mortgage2.id})

        # Check if there's only 2 campaigns in the table
        self.window.openmarket_controller.setup_view()
        self.assertEqual(self.window.openmarket_open_market_table.rowCount(), 2)

        # Check if the first campaign is in the table with the right values
        self.assertEqual(self.window.openmarket_open_market_table.item(0, 0).text(), 'straat 11, 1111AA')
        self.assertEqual(self.window.openmarket_open_market_table.item(0, 1).text(), '456')
        self.assertEqual(self.window.openmarket_open_market_table.item(0, 2).text(), '5.5')
        self.assertEqual(self.window.openmarket_open_market_table.item(0, 3).text(), '30')
        self.assertEqual(self.window.openmarket_open_market_table.item(0, 4).text(), '29')

        # Check if the second campaign is in the table with the right values
        self.assertEqual(self.window.openmarket_open_market_table.item(1, 0).text(), 'straat 11, 1111AA')
        self.assertEqual(self.window.openmarket_open_market_table.item(1, 1).text(), '456')
        self.assertEqual(self.window.openmarket_open_market_table.item(1, 2).text(), '5.5')
        self.assertEqual(self.window.openmarket_open_market_table.item(1, 3).text(), '30')
        self.assertEqual(self.window.openmarket_open_market_table.item(1, 4).text(), '29')

    def test_openmarket_view_campaign_unselected(self):
        """
        This test checks if a dialog pops up if the 'view loan bids' button in the 'open market'
        screen has been clicked without selecting a campaign
        """
        self.window.msg.about = MagicMock()
        QTest.mouseClick(self.window.openmarket_view_loan_bids_pushbutton, Qt.LeftButton)
        self.window.msg.about.assert_called_with(self.window, "Select campaign", 'No campaigns have been selected.')

    def test_openmarket_view_campaign(self):
        """
        This test checks if the 'campaign bids' screen shows when the 'view loan bids' button in
        the 'open market' screen has been clicked after selecting a campaign
        """
        # Create the investor user
        role_id = Role.INVESTOR.value
        self.window.app.user.role_id = role_id
        self.window.api.db.put(User.type, self.window.app.user.id, self.window.app.user)

        # Create a borrower
        borrower, _, _ = self.window.api.create_user()
        role_id = Role.BORROWER.value
        borrower.role_id = role_id
        self.window.api.create_profile(borrower, self.payload_borrower_profile)
        self.window.api.db.put(User.type, borrower.id, borrower)

        # Create a loan request
        borrower = self.window.api.db.get(User.type, borrower.id)
        loan_request = self.window.api.create_loan_request(borrower, self.payload_loan_request)

        # Accept the loan request
        self.payload_mortgage['user_key'] = borrower.id
        self.payload_mortgage['request_id'] = loan_request.id
        self.payload_mortgage['house_id'] = self.payload_loan_request['house_id']
        self.payload_mortgage['mortgage_type'] = self.payload_loan_request['mortgage_type']

        accepted_loan_request1, mortgage1 = self.window.api.accept_loan_request(self.window.app.bank1,
                                                                                self.payload_mortgage)

        # Accept the mortgage
        self.window.api.accept_mortgage_offer(borrower, {'mortgage_id': mortgage1.id})
        self.window.openmarket_controller.setup_view()
        self.window.openmarket_open_market_table.selectRow(0)

        # Check if the screen has been switched to the 'campaign bids screen'
        self.window.msg.about = MagicMock()
        self.window.navigation.switch_to_campaign_bids = MagicMock()
        QTest.mouseClick(self.window.openmarket_view_loan_bids_pushbutton, Qt.LeftButton)
        self.window.navigation.switch_to_campaign_bids.assert_called_with(mortgage1.id)

    def test_view_campaign_no_bids(self):
        """
        This test checks if no bids are displayed in the table in the 'campaign bids' screen
        when no bids have been offered yet
        """
        # Create the investor user
        role_id = Role.INVESTOR.value
        self.window.app.user.role_id = role_id
        self.window.api.db.put(User.type, self.window.app.user.id, self.window.app.user)

        # Create a borrower
        borrower, _, _ = self.window.api.create_user()
        role_id = Role.BORROWER.value
        borrower.role_id = role_id
        self.window.api.create_profile(borrower, self.payload_borrower_profile)
        self.window.api.db.put(User.type, borrower.id, borrower)

        # Create a loan request
        borrower = self.window.api.db.get(User.type, borrower.id)
        loan_request1 = self.window.api.create_loan_request(borrower, self.payload_loan_request)

        # Accept the loan request
        self.payload_mortgage['user_key'] = borrower.id
        self.payload_mortgage['request_id'] = loan_request1.id
        self.payload_mortgage['house_id'] = self.payload_loan_request['house_id']
        self.payload_mortgage['mortgage_type'] = self.payload_loan_request['mortgage_type']

        _, mortgage = self.window.api.accept_loan_request(self.window.app.bank1, self.payload_mortgage)

        # Accept the mortgage
        self.window.api.accept_mortgage_offer(borrower, {'mortgage_id': mortgage.id})

        # Check if there are no bids
        self.window.cb_controller.setup_view(mortgage.id)
        self.assertEqual(self.window.icb_current_bids_table.rowCount(), 0)

        # Check if the property address is correct
        self.assertEqual(self.window.icb_property_address_lineedit.text(), 'straat 11, 1111AA')

        # Check if the remaining amount is correct
        self.assertEqual(self.window.icb_remaining_amount_lineedit.text(), '456')

    def test_view_campaign_place_bid_empty(self):
        """
        This test checks if a dialog pops up when the 'place bid' button in the 'campaign bids'
        screen has been clicked without entering any information
        """
        self.create_mortgage_campaign_and_bids()
        self.window.msg.about = MagicMock()
        QTest.mouseClick(self.window.icb_place_bid_pushbutton, Qt.LeftButton)
        self.window.msg.about.assert_called_with(self.window, 'Bid error',
                                                 "You didn't enter all of the required information.")

    def test_view_campaign_place_bid_filled(self):
        """
        This test checks if a dialog pops up when the 'place bid' button in the 'campaign bids'
        screen has been clicked after entering investment information, and if the investment shows up
        in the table when the bid has been placed
        """
        # Create mortgages and bids, and fill in the bid information
        self.create_mortgage_campaign_and_bids()
        self.window.cb_controller.setup_view(self.payload_loan_offer['mortgage_id'])
        self.assertEqual(1, self.window.icb_current_bids_table.rowCount())
        self.window.msg.about = MagicMock()
        self.window.icb_amount_lineedit.setText('123')
        self.window.icb_duration_lineedit.setText('69')
        self.window.icb_interest_lineedit.setText('6.9')

        # Click the 'place bid' button
        QTest.mouseClick(self.window.icb_place_bid_pushbutton, Qt.LeftButton)
        self.window.msg.about.assert_called_with(self.window, 'Offer placed', 'Your bid has been placed.')

        # Check if the bid was added to the table
        self.assertEqual(2, self.window.icb_current_bids_table.rowCount())

        # Check if the right bid values are in the table
        self.assertEqual(self.window.icb_current_bids_table.item(1, 0).text(), '123')
        self.assertEqual(self.window.icb_current_bids_table.item(1, 1).text(), '69')
        self.assertEqual(self.window.icb_current_bids_table.item(1, 2).text(), '6.9')
        self.assertEqual(self.window.icb_current_bids_table.item(1, 3).text(), 'PENDING')

    def test_navigation_initial_visibility(self):
        """
        This test checks if the navigation bar is empty initially
        """
        navigation = NavigateUser(self.window)
        self.assertFalse(navigation.mainwindow.navigation_pushbutton_1.isVisible())
        self.assertFalse(navigation.mainwindow.navigation_pushbutton_2.isVisible())
        self.assertFalse(navigation.mainwindow.navigation_pushbutton_3.isVisible())
        self.assertFalse(navigation.mainwindow.navigation_pushbutton_4.isVisible())

    def test_navigation_switching(self):
        """
        This test checks if switching to other windows works properly
        """
        navigation = NavigateUser(self.window)

        navigation.switch_to_bplr()
        self.assertEqual(self.window.bplr_page, self.window.stackedWidget.currentWidget())

        navigation.switch_to_borrowers_portfolio()
        self.assertEqual(self.window.bp_page, self.window.stackedWidget.currentWidget())

        navigation.switch_to_investors_portfolio()
        self.assertEqual(self.window.ip_page, self.window.stackedWidget.currentWidget())

        navigation.switch_to_banks_portfolio()
        self.assertEqual(self.window.fip_page, self.window.stackedWidget.currentWidget())

        navigation.switch_to_openmarket()
        self.assertEqual(self.window.openmarket_page, self.window.stackedWidget.currentWidget())

        navigation.switch_to_profile()
        self.assertEqual(self.window.profile_page, self.window.stackedWidget.currentWidget())

        navigation.switch_to_fiplr()
        self.assertEqual(self.window.fiplr1_page, self.window.stackedWidget.currentWidget())

        navigation.switch_to_fiplr2()
        self.assertEqual(self.window.fiplr2_page, self.window.stackedWidget.currentWidget())

        self.create_mortgage_campaign_and_bids()
        navigation.switch_to_campaign_bids(self.payload_loan_offer['mortgage_id'])
        self.assertEqual(self.window.icb_page, self.window.stackedWidget.currentWidget())

    def test_navigation_user(self):
        """
        This test checks if switching between navigation bars works properly
        """
        # Check if no navigation bar has been set if the user has no role
        self.app.user.role_id = 0
        self.window.navigation.switch_to_profile = MagicMock()
        self.window.navigation.set_borrower_navigation = MagicMock()
        self.window.navigation.set_investor_navigation = MagicMock()
        self.window.navigation.set_bank_navigation = MagicMock()
        self.window.navigation.user_screen_navigation()
        self.window.navigation.switch_to_profile.assert_called()
        self.window.navigation.set_borrower_navigation.assert_not_called()
        self.window.navigation.set_investor_navigation.assert_not_called()
        self.window.navigation.set_bank_navigation.assert_not_called()

        # Check if the borrower's navigation bar has been set if the user is a borrower
        self.app.user.role_id = 1
        self.window.navigation.user_screen_navigation()
        self.window.navigation.set_borrower_navigation.assert_called()

        # Check if the investor's navigation bar has been set if the user is a investor
        self.app.user.role_id = 2
        self.window.navigation.user_screen_navigation()
        self.window.navigation.set_investor_navigation.assert_called()

        # Check if the bank's navigation bar has been set if the user is a bank
        self.app.user.role_id = 3
        self.window.navigation.user_screen_navigation()
        self.window.navigation.set_bank_navigation.assert_called()

    def test_navigation_borrower(self):
        """
        This test checks if the labels on the navigation bar are correct
        """
        self.window.navigation.set_borrower_navigation()
        self.assertEqual('Profile', self.window.navigation_pushbutton_1.text())
        self.assertEqual('Portfolio', self.window.navigation_pushbutton_2.text())
        self.assertEqual('Place Loan Request', self.window.navigation_pushbutton_3.text())
        self.assertEqual('Open Market', self.window.navigation_pushbutton_4.text())

    def test_navigation_investor(self):
        """
        This test checks if the labels on the navigation bar are correct
        """

        self.window.navigation.set_investor_navigation()
        self.assertEqual('Profile', self.window.navigation_pushbutton_1.text())
        self.assertEqual('Portfolio', self.window.navigation_pushbutton_2.text())
        self.assertEqual('Open Market', self.window.navigation_pushbutton_3.text())

    def test_navigation_bank(self):
        """
        This test checks if the labels on the navigation bar are correct
        """

        self.window.navigation.set_bank_navigation()
        self.assertEqual('Portfolio', self.window.navigation_pushbutton_1.text())
        self.assertEqual('Loan Requests', self.window.navigation_pushbutton_2.text())
        self.assertEqual('Open Market', self.window.navigation_pushbutton_3.text())

    def test_borrowers_portfolio_loans_table_empty(self):
        """
        This test checks if the ongoing loans table in the 'borrowers portfolio' screen is empty when
        the user doesn't have a loan request yet
        """
        # Check if the ongoing loans list is empty
        self.window.bp_controller.setup_view()
        self.assertFalse(self.window.bp_ongoing_loans_table.rowCount())

    def test_borrowers_portfolio_offers_table_empty(self):
        """
        This test checks if the offers table in the 'borrowers portfolio' screen is empty when the
        user doesn't have a loan request yet
        """

        # Check if the offers list is empty
        self.window.bp_controller.setup_view()
        self.assertFalse(self.window.bp_open_offers_table.rowCount())

    def test_borrowers_portfolio_offers_table_filled(self):
        """
        This test checks if the tables in the 'borrowers portfolio' screen are filled correctly.
        The ongoing loans table should only show loans that the user has accepted.
        The offers table should only show offers that the user hasn't accepted or rejected yet.
        """
        # Create the borrower user
        role_id = Role.BORROWER.value
        self.window.app.user.role_id = role_id
        self.window.api.create_profile(self.window.app.user, self.payload_borrower_profile)
        self.window.api.db.put(User.type, self.window.app.user.id, self.window.app.user)

        # Create an investor
        investor, _, _ = self.window.api.create_user()
        role_id = Role.INVESTOR.value
        investor.role_id = role_id
        self.window.api.create_profile(investor, self.payload_investor_profile)
        self.window.api.db.put(User.type, investor.id, investor)

        # Create a loan request
        self.window.app.user = self.window.api.db.get(User.type, self.window.app.user.id)
        loan_request = self.window.api.create_loan_request(self.window.app.user, self.payload_loan_request)

        # Accept the loan request
        self.payload_mortgage['user_key'] = self.window.app.user.id
        self.payload_mortgage['request_id'] = loan_request.id
        self.payload_mortgage['house_id'] = self.payload_loan_request['house_id']
        self.payload_mortgage['mortgage_type'] = self.payload_loan_request['mortgage_type']

        _, mortgage = self.window.api.accept_loan_request(self.window.app.bank1,
                                                          self.payload_mortgage)

        # Check if the mortgage shows up in the table
        self.window.bp_controller.setup_view()
        self.assertEqual(self.window.bp_open_offers_table.rowCount(), 1)

        # Check if the right values of the mortgage are in the offer table
        self.assertEqual(self.window.bp_open_offers_table.item(0, 0).text(), '123000')
        self.assertEqual(self.window.bp_open_offers_table.item(0, 1).text(), '5.5')
        self.assertEqual(self.window.bp_open_offers_table.item(0, 2).text(), '9.0')
        self.assertEqual(self.window.bp_open_offers_table.item(0, 3).text(), '30')
        self.assertEqual(self.window.bp_open_offers_table.item(0, 4).text(), u'mortgage')

        # Accept mortgage
        self.window.api.accept_mortgage_offer(self.window.app.user, {'mortgage_id': mortgage.id})

        # Place loan offer
        self.payload_loan_offer['user_key'] = investor.id  # set user_key to the investor's public key
        self.payload_loan_offer['mortgage_id'] = mortgage.id
        self.window.api.place_loan_offer(investor, self.payload_loan_offer)

        # Check if the loan offer shows up in the table
        self.window.bp_controller.setup_view()
        self.assertEqual(self.window.bp_open_offers_table.rowCount(), 1)

        # Check if the right values of the loan offer are in the offer table
        self.assertEqual(self.window.bp_open_offers_table.item(0, 0).text(), '1000')
        self.assertEqual(self.window.bp_open_offers_table.item(0, 1).text(), '2.5')
        self.assertEqual(self.window.bp_open_offers_table.item(0, 2).text(), ' ')
        self.assertEqual(self.window.bp_open_offers_table.item(0, 3).text(), '24')
        self.assertEqual(self.window.bp_open_offers_table.item(0, 4).text(), u'investment')

    def test_borrowers_portfolio_reject_unselected(self):
        """
        This test checks if a dialog pops up when the 'reject' button in the 'borrowers portfolio'
        screen has been clicked without selecting any offers
        """
        # Click the 'reject' button without selecting an item in the table
        self.window.bp_controller.setup_view()
        self.window.msg.about = MagicMock()
        QTest.mouseClick(self.window.bp_reject_pushbutton, Qt.LeftButton)

        # Check if a dialog opens
        self.window.msg.about.assert_called_with(self.window, "Select offer", 'No offers have been selected.')

    def test_borrowers_portfolio_accept_unselected(self):
        """
        This test checks if a dialog pops up when the 'accept' button in the 'borrowers portfolio'
        screen has been clicked without selecting any offers
        """
        # Click the 'reject' button without selecting an item in the table
        self.window.bp_controller.setup_view()
        self.window.msg.about = MagicMock()
        QTest.mouseClick(self.window.bp_accept_pushbutton, Qt.LeftButton)

        # Check if a dialog opens
        self.window.msg.about.assert_called_with(self.window, "Select offer", 'No offers have been selected.')

    def test_borrowers_portfolio_reject_mortgage_selected(self):
        """
        This test checks if a dialog pops up when the 'reject' button in the 'borrowers portfolio'
        screen has been clicked after selecting an offer
        """
        # Create the borrower user
        role_id = Role.BORROWER.value
        self.window.app.user.role_id = role_id
        self.window.api.create_profile(self.window.app.user, self.payload_borrower_profile)
        self.window.api.db.put(User.type, self.window.app.user.id, self.window.app.user)

        # Create an investor
        investor, _, _ = self.window.api.create_user()
        role_id = Role.INVESTOR.value
        investor.role_id = role_id
        self.window.api.create_profile(investor, self.payload_investor_profile)
        self.window.api.db.put(User.type, investor.id, investor)

        # Create a loan request
        self.window.app.user = self.window.api.db.get(User.type, self.window.app.user.id)
        loan_request = self.window.api.create_loan_request(self.window.app.user, self.payload_loan_request)

        # Accept the loan request
        self.payload_mortgage['user_key'] = self.window.app.user.id
        self.payload_mortgage['request_id'] = loan_request.id
        self.payload_mortgage['house_id'] = self.payload_loan_request['house_id']
        self.payload_mortgage['mortgage_type'] = self.payload_loan_request['mortgage_type']

        _, mortgage = self.window.api.accept_loan_request(self.window.app.bank1,
                                                          self.payload_mortgage)

        # Check if the mortgage shows up in the table
        self.window.bp_controller.setup_view()
        self.assertEqual(self.window.bp_open_offers_table.rowCount(), 1)
        self.window.bp_open_offers_table.selectRow(0)

        # Click the 'reject' button
        self.window.msg.about = MagicMock()
        QTest.mouseClick(self.window.bp_reject_pushbutton, Qt.LeftButton)

        # Check if a dialog opens
        self.window.msg.about.assert_called_with(self.window, 'Offer rejected',
                                                 'You have rejected the chosen offer')

        # Check if the mortgage has been removed from the offers table
        self.assertFalse(self.window.bp_open_offers_table.rowCount())

        # Check if the mortgage is not in the loan table
        self.assertFalse(self.window.bp_ongoing_loans_table.rowCount())

    def test_borrowers_portfolio_accept_mortgage_selected(self):
        """
        This test checks if a dialog pops up when the 'accept' button in the 'borrowers portfolio'
        screen has been clicked after selecting an offer
        """
        # Create the borrower user
        role_id = Role.BORROWER.value
        self.window.app.user.role_id = role_id
        self.window.api.create_profile(self.window.app.user, self.payload_borrower_profile)
        self.window.api.db.put(User.type, self.window.app.user.id, self.window.app.user)

        # Create an investor
        investor, _, _ = self.window.api.create_user()
        role_id = Role.INVESTOR.value
        investor.role_id = role_id
        self.window.api.create_profile(investor, self.payload_investor_profile)
        self.window.api.db.put(User.type, investor.id, investor)

        # Create a loan request
        self.window.app.user = self.window.api.db.get(User.type, self.window.app.user.id)
        loan_request = self.window.api.create_loan_request(self.window.app.user, self.payload_loan_request)

        # Accept the loan request
        self.payload_mortgage['user_key'] = self.window.app.user.id
        self.payload_mortgage['request_id'] = loan_request.id
        self.payload_mortgage['house_id'] = self.payload_loan_request['house_id']
        self.payload_mortgage['mortgage_type'] = self.payload_loan_request['mortgage_type']

        _, mortgage = self.window.api.accept_loan_request(self.window.app.bank1,
                                                          self.payload_mortgage)

        # Check if the mortgage shows up in the table
        self.window.bp_controller.setup_view()
        self.assertEqual(self.window.bp_open_offers_table.rowCount(), 1)
        self.window.bp_open_offers_table.selectRow(0)

        # Click the 'reject' button
        self.window.msg.about = MagicMock()
        QTest.mouseClick(self.window.bp_accept_pushbutton, Qt.LeftButton)

        # Check if a dialog opens
        self.window.msg.about.assert_called_with(self.window, 'Offer accepted',
                                                 'You have accepted the chosen offer')

        # Check if the mortgage has been removed from the offers table
        self.assertFalse(self.window.bp_open_offers_table.rowCount())

        # Check if the mortgage is in the loan table
        self.assertEqual(self.window.bp_ongoing_loans_table.rowCount(), 1)

    def test_borrowers_portfolio_reject_investment_selected(self):
        """
        This test checks if a dialog pops up when the 'reject' button in the 'borrowers portfolio'
        screen has been clicked after selecting an offer
        """
        # Create the borrower user
        role_id = Role.BORROWER.value
        self.window.app.user.role_id = role_id
        self.window.api.create_profile(self.window.app.user, self.payload_borrower_profile)
        self.window.api.db.put(User.type, self.window.app.user.id, self.window.app.user)

        # Create an investor
        investor, _, _ = self.window.api.create_user()
        role_id = Role.INVESTOR.value
        investor.role_id = role_id
        self.window.api.create_profile(investor, self.payload_investor_profile)
        self.window.api.db.put(User.type, investor.id, investor)

        # Create a loan request
        self.window.app.user = self.window.api.db.get(User.type, self.window.app.user.id)
        loan_request = self.window.api.create_loan_request(self.window.app.user, self.payload_loan_request)

        # Accept the loan request
        self.payload_mortgage['user_key'] = self.window.app.user.id
        self.payload_mortgage['request_id'] = loan_request.id
        self.payload_mortgage['house_id'] = self.payload_loan_request['house_id']
        self.payload_mortgage['mortgage_type'] = self.payload_loan_request['mortgage_type']

        _, mortgage = self.window.api.accept_loan_request(self.window.app.bank1,
                                                          self.payload_mortgage)

        # Accept mortgage
        self.window.api.accept_mortgage_offer(self.window.app.user, {'mortgage_id': mortgage.id})

        # Place loan offer
        self.payload_loan_offer['user_key'] = investor.id  # set user_key to the investor's public key
        self.payload_loan_offer['mortgage_id'] = mortgage.id
        self.window.api.place_loan_offer(investor, self.payload_loan_offer)

        # Check if the loan offer shows up in the table
        self.window.bp_controller.setup_view()
        self.assertEqual(self.window.bp_open_offers_table.rowCount(), 1)
        self.window.bp_open_offers_table.selectRow(0)

        # Click the 'reject' button
        self.window.msg.about = MagicMock()
        QTest.mouseClick(self.window.bp_reject_pushbutton, Qt.LeftButton)

        # Check if a dialog opens
        self.window.msg.about.assert_called_with(self.window, 'Offer rejected',
                                                 'You have rejected the chosen offer')

        # Check if the mortgage has been removed from the offers table
        self.assertFalse(self.window.bp_open_offers_table.rowCount())

        # Check if the investment is not in the loan table
        self.assertEqual(self.window.bp_ongoing_loans_table.rowCount(), 1)

    def test_borrowers_portfolio_accept_investment_selected(self):
        """
        This test checks if a dialog pops up when the 'accept' button in the 'borrowers portfolio'
        screen has been clicked after selecting an offer
        """
        # Create the borrower user
        role_id = Role.BORROWER.value
        self.window.app.user.role_id = role_id
        self.window.api.create_profile(self.window.app.user, self.payload_borrower_profile)
        self.window.api.db.put(User.type, self.window.app.user.id, self.window.app.user)

        # Create an investor
        investor, _, _ = self.window.api.create_user()
        role_id = Role.INVESTOR.value
        investor.role_id = role_id
        self.window.api.create_profile(investor, self.payload_investor_profile)
        self.window.api.db.put(User.type, investor.id, investor)

        # Create a loan request
        self.window.app.user = self.window.api.db.get(User.type, self.window.app.user.id)
        loan_request = self.window.api.create_loan_request(self.window.app.user, self.payload_loan_request)

        # Accept the loan request
        self.payload_mortgage['user_key'] = self.window.app.user.id
        self.payload_mortgage['request_id'] = loan_request.id
        self.payload_mortgage['house_id'] = self.payload_loan_request['house_id']
        self.payload_mortgage['mortgage_type'] = self.payload_loan_request['mortgage_type']

        _, mortgage = self.window.api.accept_loan_request(self.window.app.bank1,
                                                          self.payload_mortgage)

        # Accept mortgage
        self.window.api.accept_mortgage_offer(self.window.app.user, {'mortgage_id': mortgage.id})

        # Place loan offer
        self.payload_loan_offer['user_key'] = investor.id  # set user_key to the investor's public key
        self.payload_loan_offer['mortgage_id'] = mortgage.id
        self.window.api.place_loan_offer(investor, self.payload_loan_offer)

        # Check if the loan offer shows up in the table
        self.window.bp_controller.setup_view()
        self.assertEqual(self.window.bp_open_offers_table.rowCount(), 1)
        self.window.bp_open_offers_table.selectRow(0)

        # Click the 'reject' button
        self.window.msg.about = MagicMock()
        QTest.mouseClick(self.window.bp_accept_pushbutton, Qt.LeftButton)

        # Check if a dialog opens
        self.window.msg.about.assert_called_with(self.window, 'Offer accepted',
                                                 'You have accepted the chosen offer')

        # Check if the investment has been removed from the offers table
        self.assertFalse(self.window.bp_open_offers_table.rowCount())

        # Check if the investment is in the loan table (that already contained the mortgage)
        self.assertEqual(self.window.bp_ongoing_loans_table.rowCount(), 2)

    def test_investors_portfolio_table_empty(self):
        """
        This test checks if the table in the 'investors portfolio' screen is empty when the
        user hasn't placed any bids yet
        """
        # Check if the investments list is empty
        self.window.ip_controller.setup_view()
        self.assertFalse(self.window.ip_investments_table.rowCount())

    def test_investors_portfolio_table_filled(self):
        """
        This test checks if the table in the 'investors portfolio' screen has been filled
        after the user has placed bids
        """
        # Create the investor user
        role_id = Role.INVESTOR.value
        self.window.app.user.role_id = role_id
        self.window.api.create_profile(self.window.app.user, self.payload_investor_profile)
        self.window.api.db.put(User.type, self.window.app.user.id, self.window.app.user)

        # Create borrowers
        borrower1, _, _ = self.window.api.create_user()
        role_id = Role.BORROWER.value
        borrower1.role_id = role_id
        self.window.api.create_profile(borrower1, self.payload_borrower_profile)
        self.window.api.db.put(User.type, borrower1.id, borrower1)

        borrower2, _, _ = self.window.api.create_user()
        borrower2.role_id = role_id
        self.window.api.create_profile(borrower2, self.payload_borrower_profile)
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
        self.window.api.accept_mortgage_offer(borrower1, {'mortgage_id': mortgage1.id})
        self.window.api.accept_mortgage_offer(borrower2, {'mortgage_id': mortgage2.id})

        # Place loan offers
        self.payload_loan_offer['user_key'] = self.window.app.user.id  # set user_key to the investor's public key
        self.payload_loan_offer['mortgage_id'] = mortgage1.id
        self.window.api.place_loan_offer(self.window.app.user, self.payload_loan_offer)

        self.payload_loan_offer['mortgage_id'] = mortgage2.id
        self.payload_loan_offer['amount'] = 123456
        loan_offer2 = self.window.api.place_loan_offer(self.window.app.user, self.payload_loan_offer)

        # Accept one of the loan offers
        self.window.api.accept_investment_offer(borrower2, {'investment_id': loan_offer2.id})

        # Check if there's only 2 investments in the table
        self.window.ip_controller.setup_view()
        self.assertEqual(self.window.ip_investments_table.rowCount(), 2)

        # Check if the first investment is in the table with the right values
        self.assertEqual(self.window.ip_investments_table.item(0, 0).text(), 'straat 11, 1111AA')
        self.assertEqual(self.window.ip_investments_table.item(0, 1).text(), 'Running')
        self.assertEqual(self.window.ip_investments_table.item(0, 2).text(), 'Pending')
        self.assertEqual(self.window.ip_investments_table.item(0, 3).text(), '1000')
        self.assertEqual(self.window.ip_investments_table.item(0, 4).text(), '2.5')
        self.assertEqual(self.window.ip_investments_table.item(0, 5).text(), '24')
        self.assertEqual(self.window.ip_investments_table.item(0, 6).text(), ' ')
        self.assertEqual(self.window.ip_investments_table.item(0, 7).text(), ' ')

        # Check if the second investment is in the table with the right values
        self.assertEqual(self.window.ip_investments_table.item(1, 0).text(), 'straat 11, 1111AA')
        self.assertEqual(self.window.ip_investments_table.item(1, 1).text(), 'Completed')
        self.assertEqual(self.window.ip_investments_table.item(1, 2).text(), 'Accepted')
        self.assertEqual(self.window.ip_investments_table.item(1, 3).text(), '123456')
        self.assertEqual(self.window.ip_investments_table.item(1, 4).text(), '2.5')
        self.assertEqual(self.window.ip_investments_table.item(1, 5).text(), '24')
        self.assertEqual(self.window.ip_investments_table.item(1, 6).text(), 'Bob Saget')
        self.assertEqual(self.window.ip_investments_table.item(1, 7).text(), 'NL53 INGBB 04027 30393')

    def test_banks_portfolio_table_empty(self):
        """
        This test checks if the table in the 'banks portfolio' screen is empty when
        the user doesn't have any accepted mortgages yet
        """
        # Check if the mortgage list is empty
        self.window.fip_controller.setup_view()
        self.assertFalse(self.window.fip_campaigns_table.rowCount())

    def test_banks_portfolio_table_filled(self):
        """
        This test checks if the table in the 'investors portfolio' screen has been filled
        after the user has placed bids
        """
        # Create the bank user
        self.window.app.user = self.window.app.bank1

        # Create borrowers
        borrower1, _, _ = self.window.api.create_user()
        role_id = Role.BORROWER.value
        borrower1.role_id = role_id
        self.window.api.create_profile(borrower1, self.payload_borrower_profile)
        self.window.api.db.put(User.type, borrower1.id, borrower1)

        borrower2, _, _ = self.window.api.create_user()
        borrower2.role_id = role_id
        self.window.api.create_profile(borrower2, self.payload_borrower_profile)
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
        self.window.api.accept_mortgage_offer(borrower1, {'mortgage_id': mortgage1.id})
        self.window.api.accept_mortgage_offer(borrower2, {'mortgage_id': mortgage2.id})

        # Create an investor
        investor, _, _ = self.window.api.create_user()
        role_id = Role.INVESTOR.value
        investor.role_id = role_id
        self.window.api.create_profile(investor, self.payload_investor_profile)
        self.window.api.db.put(User.type, investor.id, investor)

        # Place loan offer
        self.payload_loan_offer['user_key'] = investor.id  # set user_key to the investor's public key
        self.payload_loan_offer['mortgage_id'] = mortgage1.id
        loan_offer = self.window.api.place_loan_offer(investor, self.payload_loan_offer)

        # Accept the loan offer
        self.window.api.accept_investment_offer(borrower1, {'investment_id': loan_offer.id})

        # Check if there's only 2 mortgages in the table
        self.window.fip_controller.setup_view()
        self.assertEqual(self.window.fip_campaigns_table.rowCount(), 2)

        # Check if the first mortgage is in the table with the right values
        self.assertEqual(self.window.fip_campaigns_table.item(0, 0).text(), 'straat 11, 1111AA')
        self.assertEqual(self.window.fip_campaigns_table.item(0, 1).text(), 'Completed')
        self.assertEqual(self.window.fip_campaigns_table.item(0, 2).text(), '123000')
        self.assertEqual(self.window.fip_campaigns_table.item(0, 3).text(), '5.5')
        self.assertEqual(self.window.fip_campaigns_table.item(0, 4).text(), '9.0')
        self.assertEqual(self.window.fip_campaigns_table.item(0, 5).text(), '30')
        self.assertEqual(self.window.fip_campaigns_table.item(0, 6).text(), 'Bob Saget')
        self.assertEqual(self.window.fip_campaigns_table.item(0, 7).text(), 'NL53 INGBB 04027 30393')

        # Check if the second mortgage is in the table with the right values
        self.assertEqual(self.window.fip_campaigns_table.item(1, 0).text(), 'straat 11, 1111AA')
        self.assertEqual(self.window.fip_campaigns_table.item(1, 1).text(), 'Running')
        self.assertEqual(self.window.fip_campaigns_table.item(1, 2).text(), '123000')
        self.assertEqual(self.window.fip_campaigns_table.item(1, 3).text(), '5.5')
        self.assertEqual(self.window.fip_campaigns_table.item(1, 4).text(), '9.0')
        self.assertEqual(self.window.fip_campaigns_table.item(1, 5).text(), '30')
        self.assertEqual(self.window.fip_campaigns_table.item(1, 6).text(), 'Bob Saget')
        self.assertEqual(self.window.fip_campaigns_table.item(1, 7).text(), 'NL53 INGBB 04027 30393')

    def test_pending_loan_requests_table_empty(self):
        """
        This test checks if the table in the 'pending loan requests' screen is empty when there are
        no open loan requests
        """
        # Check if the loan request list is empty
        self.window.fiplr1_controller.setup_view()
        self.assertFalse(self.window.fiplr1_loan_requests_table.rowCount())

    def test_pending_loan_requests_table_filled(self):
        """
        This test checks if the table in the 'pending loan requests' screen has been filled when the
        user has open loan requests
        """
        # Create the bank user
        self.window.app.user = self.window.app.bank1

        # Create borrowers
        borrower1, _, _ = self.window.api.create_user()
        role_id = Role.BORROWER.value
        borrower1.role_id = role_id
        self.window.api.create_profile(borrower1, self.payload_borrower_profile)
        self.window.api.db.put(User.type, borrower1.id, borrower1)

        borrower2, _, _ = self.window.api.create_user()
        borrower2.role_id = role_id
        self.window.api.create_profile(borrower2, self.payload_borrower_profile)
        self.window.api.db.put(User.type, borrower2.id, borrower2)

        # Create loan requests
        borrower1 = self.window.api.db.get(User.type, borrower1.id)
        self.window.api.create_loan_request(borrower1, self.payload_loan_request)

        borrower2 = self.window.api.db.get(User.type, borrower2.id)
        self.payload_loan_request['mortgage_type'] = 2
        self.window.api.create_loan_request(borrower2, self.payload_loan_request)

        # Check if there are only 2 loan requests in the table
        self.window.fiplr1_controller.setup_view()
        self.assertEqual(self.window.fiplr1_loan_requests_table.rowCount(), 2)

        # Check if the first loan request is in the table with the right values
        self.assertEqual(self.window.fiplr1_loan_requests_table.item(0, 0).text(), 'straat 11, 1111AA')
        self.assertEqual(self.window.fiplr1_loan_requests_table.item(0, 1).text(), 'Linear')
        self.assertEqual(self.window.fiplr1_loan_requests_table.item(0, 2).text(), '123456')
        self.assertEqual(self.window.fiplr1_loan_requests_table.item(0, 3).text(), '123456')

        # Check if the second loan request is in the table with the right values
        self.assertEqual(self.window.fiplr1_loan_requests_table.item(1, 0).text(), 'straat 11, 1111AA')
        self.assertEqual(self.window.fiplr1_loan_requests_table.item(1, 1).text(), 'Fixed-Rate')
        self.assertEqual(self.window.fiplr1_loan_requests_table.item(1, 2).text(), '123456')
        self.assertEqual(self.window.fiplr1_loan_requests_table.item(1, 3).text(), '123456')

    def test_pending_loan_requests_table_unselected(self):
        """
        This test checks if a dialog pops up when the 'view loan request' button in the
        'pending loan request' has been clicked when no loan requests have been selected
        """
        # Click the 'view loan request' button without selecting an item in the table
        self.window.fiplr1_controller.setup_view()
        self.window.msg.about = MagicMock()
        QTest.mouseClick(self.window.fiplr1_view_loan_request_pushbutton, Qt.LeftButton)

        # Check if a dialog opens
        self.window.msg.about.assert_called_with(self.window, "Select request",
                                                 'No loan requests have been selected.')

    def test_pending_loan_requests_table_selected(self):
        """
        This test checks if the 'pending loan request' screen is showed when clicking on the
        'view loan request' button after selecting a loan request
        """
        # Create the bank user
        self.window.app.user = self.window.app.bank1

        # Create a borrower
        borrower, _, _ = self.window.api.create_user()
        role_id = Role.BORROWER.value
        borrower.role_id = role_id
        self.window.api.create_profile(borrower, self.payload_borrower_profile)
        self.window.api.db.put(User.type, borrower.id, borrower)

        # Create a loan request
        borrower = self.window.api.db.get(User.type, borrower.id)
        loan_request = self.window.api.create_loan_request(borrower, self.payload_loan_request)

        # Select the item on the first row in the table
        self.window.fiplr1_controller.setup_view()
        self.window.fiplr1_loan_requests_table.selectRow(0)

        # Click the 'view loan request' button
        self.window.msg.about = MagicMock()
        self.window.fiplr2_controller.setup_view = MagicMock()
        QTest.mouseClick(self.window.fiplr1_view_loan_request_pushbutton, Qt.LeftButton)

        # Check if the 'pending loan request' view has been called
        self.window.fiplr2_controller.setup_view.assert_called_with(loan_request.id)

    def test_pending_loan_request_forms_filled_linear(self):
        """
        This test checks if the fields in the 'pending loan request' screen are filled correctly
        """
        # Add documents
        self.window.fiplr2_controller.search = lambda x: ['TestDocument1.pdf',
                                                          'TestDocument2.pdf',
                                                          'TestDocument3.pdf']

        # Create the bank user
        self.window.app.user = self.window.app.bank1

        # Create a borrower with profile
        borrower, _, _ = self.window.api.create_user()
        role_id = Role.BORROWER.value
        borrower.role_id = role_id
        self.window.api.db.put(User.type, borrower.id, borrower)
        self.window.api.create_profile(borrower, self.payload_borrower_profile)

        # Create a loan request
        borrower = self.window.api.db.get(User.type, borrower.id)
        loan_request = self.window.api.create_loan_request(borrower, self.payload_loan_request)

        # Check if all the fields are filled in with the right information
        self.window.fiplr2_controller.setup_view(loan_request.id)
        self.assertEqual(self.window.fiplr2_firstname_lineedit.text(), u'Bob')
        self.assertEqual(self.window.fiplr2_lastname_lineedit.text(), u'Saget')
        self.assertEqual(self.window.fiplr2_address_lineedit.text(), 'straat 22, 2162CD')
        self.assertEqual(self.window.fiplr2_phonenumber_lineedit.text(), '+3170253719234')
        self.assertEqual(self.window.fiplr2_email_lineedit.text(), 'example@example.com')
        self.assertEqual(self.window.fiplr2_property_address_lineedit.text(), 'straat 11, 1111AA')
        self.assertEqual(self.window.fiplr2_loan_amount_lineedit.text(), '123456')
        self.assertEqual(self.window.fiplr2_mortgage_type_lineedit.text(), 'Linear')
        self.assertEqual(self.window.fiplr2_property_value_lineedit.text(), '123456')
        self.assertEqual(self.window.fiplr2_description_textedit.toPlainText(), u'I want to buy a house')

    def test_pending_loan_request_forms_filled_fixedrate(self):
        """
        This test checks if the fields in the 'pending loan request' screen are filled correctly
        """
        # Add documents
        self.window.fiplr2_controller.search = lambda x: ['TestDocument1.pdf',
                                                          'TestDocument2.pdf',
                                                          'TestDocument3.pdf']

        # Create the bank user
        self.window.app.user = self.window.app.bank1

        # Create a borrower with profile
        borrower, _, _ = self.window.api.create_user()
        role_id = Role.BORROWER.value
        borrower.role_id = role_id
        self.window.api.db.put(User.type, borrower.id, borrower)
        self.window.api.create_profile(borrower, self.payload_borrower_profile)

        # Create a loan request
        borrower = self.window.api.db.get(User.type, borrower.id)
        self.payload_loan_request['mortgage_type'] = 2
        loan_request = self.window.api.create_loan_request(borrower, self.payload_loan_request)

        # Check if all the fields are filled in with the right information
        self.window.fiplr2_controller.setup_view(loan_request.id)
        self.assertEqual(self.window.fiplr2_firstname_lineedit.text(), u'Bob')
        self.assertEqual(self.window.fiplr2_lastname_lineedit.text(), u'Saget')
        self.assertEqual(self.window.fiplr2_address_lineedit.text(), 'straat 22, 2162CD')
        self.assertEqual(self.window.fiplr2_phonenumber_lineedit.text(), '+3170253719234')
        self.assertEqual(self.window.fiplr2_email_lineedit.text(), 'example@example.com')
        self.assertEqual(self.window.fiplr2_property_address_lineedit.text(), 'straat 11, 1111AA')
        self.assertEqual(self.window.fiplr2_loan_amount_lineedit.text(), '123456')
        self.assertEqual(self.window.fiplr2_mortgage_type_lineedit.text(), 'Fixed-Rate')
        self.assertEqual(self.window.fiplr2_property_value_lineedit.text(), '123456')
        self.assertEqual(self.window.fiplr2_description_textedit.toPlainText(), u'I want to buy a house')

    def test_pending_loan_request_accept_empty(self):
        """
        This test checks if a dialog pops up when clicking the 'accept' button in the 'pending loan request'
        screen without entering any information
        """
        # Create the bank user
        self.window.app.user = self.window.app.bank1

        # Create a borrower with profile
        borrower, _, _ = self.window.api.create_user()
        role_id = Role.BORROWER.value
        borrower.role_id = role_id
        self.window.api.db.put(User.type, borrower.id, borrower)
        self.window.api.create_profile(borrower, self.payload_borrower_profile)

        # Create a loan request
        borrower = self.window.api.db.get(User.type, borrower.id)
        self.payload_loan_request['mortgage_type'] = 2
        loan_request = self.window.api.create_loan_request(borrower, self.payload_loan_request)

        # Click the 'accept' button without filling in any mortgage info
        self.window.fiplr2_controller.setup_view(loan_request.id)
        self.window.msg.about = MagicMock()
        QTest.mouseClick(self.window.fiplr2_accept_pushbutton, Qt.LeftButton)

        # Check if a dialog opens
        self.window.msg.about.assert_called_with(self.window, "Loan request error",
                                                 'You didn\'t enter all of the required information.')

    def test_pending_loan_request_accept_filled(self):
        """
        This test checks if a dialog pops up when clicking the 'accept' button in the 'pending loan request'
        screen after entering mortgage information
        """
        # Create the bank user
        self.window.app.user = self.window.app.bank1

        # Create a borrower with profile
        borrower, _, _ = self.window.api.create_user()
        role_id = Role.BORROWER.value
        borrower.role_id = role_id
        self.window.api.db.put(User.type, borrower.id, borrower)
        self.window.api.create_profile(borrower, self.payload_borrower_profile)

        # Create a loan request
        borrower = self.window.api.db.get(User.type, borrower.id)
        self.payload_loan_request['mortgage_type'] = 2
        loan_request = self.window.api.create_loan_request(borrower, self.payload_loan_request)

        # Fill in mortgage info
        self.window.fiplr2_offer_amount_lineedit.setText('123000')
        self.window.fiplr2_offer_interest_lineedit.setText('2.1')
        self.window.fiplr2_default_rate_lineedit.setText('3.9')
        self.window.fiplr2_loan_duration_lineedit.setText('300')

        # Click the 'accept' button
        self.window.fiplr2_controller.setup_view(loan_request.id)
        self.window.msg.about = MagicMock()
        QTest.mouseClick(self.window.fiplr2_accept_pushbutton, Qt.LeftButton)

        # Check if a dialog opens
        self.window.msg.about.assert_called_with(self.window, "Request accepted",
                                                 'This loan request has been accepted.')

    def test_pending_loan_request_reject(self):
        """
        This test checks if a dialog pops up when clicking the 'reject' button in the 'pending loan request' screen
        """
        # Create the bank user
        self.window.app.user = self.window.app.bank1

        # Create a borrower with profile
        borrower, _, _ = self.window.api.create_user()
        role_id = Role.BORROWER.value
        borrower.role_id = role_id
        self.window.api.db.put(User.type, borrower.id, borrower)
        self.window.api.create_profile(borrower, self.payload_borrower_profile)

        # Create a loan request
        borrower = self.window.api.db.get(User.type, borrower.id)
        self.payload_loan_request['mortgage_type'] = 2
        loan_request = self.window.api.create_loan_request(borrower, self.payload_loan_request)
        self.window.app.user = self.window.api.db.get(User.type, self.window.app.user.id)

        # Click the 'reject' button
        self.window.fiplr2_controller.setup_view(loan_request.id)
        self.window.msg.about = MagicMock()
        QTest.mouseClick(self.window.fiplr2_reject_pushbutton, Qt.LeftButton)

        # Check if a dialog opens
        self.window.msg.about.assert_called_with(self.window, "Request rejected",
                                                 'This loan request has been rejected.')

    def test_page_setup_borrower(self):
        """
        This test checks if the right screen is displayed if the user logs in as borrower
        """
        # Create the user
        self.window.app.user, _, _ = self.window.api.create_user()
        role_id = Role.BORROWER.value
        self.window.app.user.role_id = role_id
        self.window.api.create_profile(self.window.app.user, self.payload_borrower_profile)
        self.window.api.db.put(User.type, self.window.app.user.id, self.window.app.user)

        # Check is the right screen is being displayed
        self.window.setup_view()
        self.assertEqual(self.window.profile_page, self.window.stackedWidget.currentWidget())

    def test_page_setup_investor(self):
        """
        This test checks if the right screen is displayed if the user logs in as investor
        """
        # Create the user
        self.window.app.user, _, _ = self.window.api.create_user()
        role_id = Role.INVESTOR.value
        self.window.app.user.role_id = role_id
        self.window.api.create_profile(self.window.app.user, self.payload_investor_profile)
        self.window.api.db.put(User.type, self.window.app.user.id, self.window.app.user)

        # Check is the right screen is being displayed
        self.window.setup_view()
        self.assertEqual(self.window.profile_page, self.window.stackedWidget.currentWidget())

    def test_page_setup_bank(self):
        """
        This test checks if the right screen is displayed if the user logs in as bank
        """
        # Create the user
        self.window.app.user, _, _ = self.window.api.create_user()
        role_id = Role.FINANCIAL_INSTITUTION.value
        self.window.app.user.role_id = role_id
        self.window.api.db.put(User.type, self.window.app.user.id, self.window.app.user)

        # Check is the right screen is being displayed
        self.window.setup_view()
        self.assertEqual(self.window.fip_page, self.window.stackedWidget.currentWidget())

    def test_filter_table(self):
        # detach the controller so we can do some preparing without triggering anything
        self.window.openmarket_controller = None
        table = self.window.openmarket_open_market_table
        function2 = MainWindowController.filter_matching
        function3 = MainWindowController.filter_in_range
        mock1 = MagicMock()
        mock2 = MagicMock()
        MainWindowController.filter_matching = mock1
        MainWindowController.filter_in_range = mock2

        # set some input in the lineedits without triggering them
        self.window.openmarket_max_amount_lineedit.setText('3')
        self.window.openmarket_min_amount_lineedit.setText('1')
        self.window.openmarket_interest1_lineedit.setText('1.1')
        self.window.openmarket_interest2_lineedit.setText('2.2')
        self.window.openmarket_duration1_lineedit.setText('9')
        self.window.openmarket_duration2_lineedit.setText('12')

        self.window.openmarket_controller = OpenMarketController(self.window)
        self.assertFalse(self.window.openmarket_search_lineedit.text(), 'a')
        QTest.keyClicks(self.window.openmarket_search_lineedit, 'a')
        self.assertTrue(self.window.openmarket_search_lineedit.text(), 'a')

        mock1.assert_called_once_with(table, 'a')
        mock2.assert_called_with(table, 3, '9', '12')
        MainWindowController.filter_matching = function2
        MainWindowController.filter_in_range = function3

    def test_show_hidden(self):
        table = self.window.openmarket_open_market_table
        table.setRowCount(0)
        self.window.openmarket_search_lineedit.setText('')
        self.window.openmarket_max_amount_lineedit.setText('')
        self.window.openmarket_min_amount_lineedit.setText('')
        self.window.openmarket_interest1_lineedit.setText('')
        self.window.openmarket_interest2_lineedit.setText('')
        self.window.openmarket_duration1_lineedit.setText('')
        self.window.openmarket_duration2_lineedit.setText('')
        MainWindowController.insert_row(table, ['LaanStraat', '50', '1.0', '12', '3'])
        MainWindowController.insert_row(table, ['AStraat', '450', '3.0', '12', '9'])
        MainWindowController.insert_row(table, ['CStraat', '560', '1.5', '24', '3'])
        self.assertEqual(table.rowCount(), 3)
        self.assertFalse(table.isRowHidden(0))
        self.assertFalse(table.isRowHidden(1))
        self.assertFalse(table.isRowHidden(2))
        table.hideRow(0)
        table.hideRow(1)
        table.hideRow(2)
        self.assertTrue(table.isRowHidden(0))
        self.assertTrue(table.isRowHidden(1))
        self.assertTrue(table.isRowHidden(2))
        self.assertEqual(table.rowCount(), 3)
        MainWindowController.show_hidden(table)
        self.assertEqual(table.rowCount(), 3)
        self.assertFalse(table.isRowHidden(0))
        self.assertFalse(table.isRowHidden(1))
        self.assertFalse(table.isRowHidden(2))

    def test_filter_matched(self):
        table = self.window.openmarket_open_market_table
        MainWindowController.insert_row(table, ['LaanStraat', '50', '1.0', '12', '3'])
        MainWindowController.insert_row(table, ['AStraat', '450', '3.0', '12', '9'])
        MainWindowController.insert_row(table, ['BStraat', '560', '1.5', '24', '3'])
        self.assertEqual(table.rowCount(), 3)
        self.assertFalse(table.isRowHidden(0))
        self.assertFalse(table.isRowHidden(1))
        self.assertFalse(table.isRowHidden(2))
        self.window.openmarket_search_lineedit.setText('ABC')
        self.assertTrue(table.isRowHidden(0))
        self.assertTrue(table.isRowHidden(1))
        self.assertTrue(table.isRowHidden(2))
        self.window.openmarket_search_lineedit.setText('Straat')
        self.assertFalse(table.isRowHidden(0))
        self.assertFalse(table.isRowHidden(1))
        self.assertFalse(table.isRowHidden(2))
        self.window.openmarket_search_lineedit.setText('AStraat')
        self.assertTrue(table.isRowHidden(0))
        self.assertFalse(table.isRowHidden(1))
        self.assertTrue(table.isRowHidden(2))
        self.window.openmarket_search_lineedit.setText('')
        self.assertFalse(table.isRowHidden(0))
        self.assertFalse(table.isRowHidden(1))
        self.assertFalse(table.isRowHidden(2))

    def test_filter_in_range(self):
        table = self.window.openmarket_open_market_table
        MainWindowController.insert_row(table, ['LaanStraat', '50', '1.0', '12', '3'])
        MainWindowController.insert_row(table, ['AStraat', '450', '3.0', '12', '9'])
        MainWindowController.insert_row(table, ['BStraat', '560', '1.5', '24', '3'])
        self.assertEqual(table.rowCount(), 3)
        self.assertFalse(table.isRowHidden(0))
        self.assertFalse(table.isRowHidden(1))
        self.assertFalse(table.isRowHidden(2))
        self.window.openmarket_max_amount_lineedit.setText('500')
        self.window.openmarket_min_amount_lineedit.setText('1')
        self.assertFalse(table.isRowHidden(0))
        self.assertFalse(table.isRowHidden(1))
        self.assertTrue(table.isRowHidden(2))
        self.window.openmarket_interest1_lineedit.setText('0.9')
        self.window.openmarket_interest2_lineedit.setText('2.2')
        self.assertFalse(table.isRowHidden(0))
        self.assertTrue(table.isRowHidden(1))
        self.assertTrue(table.isRowHidden(2))
        self.window.openmarket_duration1_lineedit.setText('9')
        self.window.openmarket_duration2_lineedit.setText('a')
        self.assertFalse(table.isRowHidden(0))
        self.assertTrue(table.isRowHidden(1))
        self.assertTrue(table.isRowHidden(2))
        self.window.openmarket_duration1_lineedit.setText('9')
        self.window.openmarket_duration2_lineedit.setText('11')
        self.assertTrue(table.isRowHidden(0))
        self.assertTrue(table.isRowHidden(1))
        self.assertTrue(table.isRowHidden(2))
        self.window.openmarket_max_amount_lineedit.setText('')
        self.window.openmarket_min_amount_lineedit.setText('')
        self.window.openmarket_interest1_lineedit.setText('')
        self.window.openmarket_interest2_lineedit.setText('')
        self.window.openmarket_duration1_lineedit.setText('')
        self.window.openmarket_duration2_lineedit.setText('')
        self.assertFalse(table.isRowHidden(0))
        self.assertFalse(table.isRowHidden(1))
        self.assertFalse(table.isRowHidden(2))
        self.assertEqual(table.rowCount(), 3)

    def test_filter_combo(self):
        table = self.window.openmarket_open_market_table
        MainWindowController.insert_row(table, ['LaanStraat', '50', '1.0', '12', '3'])
        MainWindowController.insert_row(table, ['AnStraat', '450', '3.0', '12', '9'])
        MainWindowController.insert_row(table, ['BaStraat', '560', '1.5', '24', '3'])
        MainWindowController.insert_row(table, ['CaStraat', '75', '5.5', '9', '5'])
        MainWindowController.insert_row(table, ['DnStraat', '350', '1.5', '36', '4'])
        self.assertEqual(table.rowCount(), 5)
        self.assertFalse(table.isRowHidden(0))
        self.assertFalse(table.isRowHidden(1))
        self.assertFalse(table.isRowHidden(2))
        self.assertFalse(table.isRowHidden(3))
        self.assertFalse(table.isRowHidden(4))
        self.window.openmarket_max_amount_lineedit.setText('500')
        self.window.openmarket_min_amount_lineedit.setText('1')
        self.assertFalse(table.isRowHidden(0))
        self.assertFalse(table.isRowHidden(1))
        self.assertTrue(table.isRowHidden(2))
        self.assertFalse(table.isRowHidden(3))
        self.assertFalse(table.isRowHidden(4))
        self.window.openmarket_search_lineedit.setText('nS')
        self.assertFalse(table.isRowHidden(0))
        self.assertFalse(table.isRowHidden(1))
        self.assertTrue(table.isRowHidden(2))
        self.assertTrue(table.isRowHidden(3))
        self.assertFalse(table.isRowHidden(4))
        self.window.openmarket_interest1_lineedit.setText('0.9')
        self.window.openmarket_interest2_lineedit.setText('2.4')
        self.assertFalse(table.isRowHidden(0))
        self.assertTrue(table.isRowHidden(1))
        self.assertTrue(table.isRowHidden(2))
        self.assertTrue(table.isRowHidden(3))
        self.assertFalse(table.isRowHidden(4))
        self.window.openmarket_duration1_lineedit.setText('40')
        self.window.openmarket_duration2_lineedit.setText('60')
        self.assertTrue(table.isRowHidden(0))
        self.assertTrue(table.isRowHidden(1))
        self.assertTrue(table.isRowHidden(2))
        self.assertTrue(table.isRowHidden(3))
        self.assertTrue(table.isRowHidden(4))
        self.window.openmarket_search_lineedit.setText('')
        self.window.openmarket_max_amount_lineedit.setText('')
        self.window.openmarket_min_amount_lineedit.setText('')
        self.window.openmarket_interest1_lineedit.setText('')
        self.window.openmarket_interest2_lineedit.setText('')
        self.window.openmarket_duration1_lineedit.setText('')
        self.window.openmarket_duration2_lineedit.setText('')
        self.assertFalse(table.isRowHidden(0))
        self.assertFalse(table.isRowHidden(1))
        self.assertFalse(table.isRowHidden(2))
        self.assertFalse(table.isRowHidden(3))
        self.assertFalse(table.isRowHidden(4))
        self.assertEqual(table.rowCount(), 5)
