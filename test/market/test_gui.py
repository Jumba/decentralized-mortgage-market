from __future__ import absolute_import

import os
import sys
import unittest
from uuid import UUID

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QTableWidget

from market.api.api import STATUS
from market.controllers.main_view_controller import MainWindowController
from market.controllers.navigation import NavigateUser
from market.models.loans import Mortgage
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
        self.payload_borrower_profile = {'role': 1, 'first_name': u'Bob', 'last_name': u'Saget',
                                         'email': 'example@example.com', 'iban': 'NL53 INGBB 04027 30393',
                                         'phonenumber': '+3170253719234', 'current_postalcode': '2162CD',
                                         'current_housenumber': '22', 'current_address': 'straat',
                                         'documents_list': []}
        self.payload_investor_profile = {'role': 2, 'first_name': u'Ruby', 'last_name': u'Cue',
                                         'email': 'example1@example.com', 'iban': 'NL53 INGBB 04027 30393',
                                         'phonenumber': '+3170253719290'}
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

    def tearDown(self):
        pass

    def test_profile_empty(self):
        # Test that the controller calls a QMessageBox with unique input when the form has not been filled in
        self.window.msg.about = MagicMock()
        QTest.mouseClick(self.window.profile_save_pushbutton, Qt.LeftButton)
        self.window.msg.about.assert_called_with(self.window, 'Profile error', 'You didn\'t enter all of the required information.')

    def test_profile_create_profile(self):
        # Testing loading of the current borrower's profile
        self.assertEqual(None, self.window.profile_controller.current_profile)

        # Create profile so when we can populate the form easier
        user, _, _ = self.app.api.create_user()
        profile = self.app.api.create_profile(user, self.payload_borrower_profile)
        self.assertNotEqual(None, profile)

        # Fill in the form and press the 'save'-button
        self.window.profile_controller.update_form(profile)
        self.window.msg.about = MagicMock()
        QTest.mouseClick(self.window.profile_save_pushbutton, Qt.LeftButton)
        self.window.msg.about.assert_called_with(self.window, 'Profile saved', 'Your profile has been saved.')

    def test_profile_load_current_borrower(self):
        # Testing loading of the current borrower's profile
        self.assertEqual(None, self.window.profile_controller.current_profile)
        profile = self.app.api.create_profile(self.app.user, self.payload_borrower_profile)
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

        profile = self.app.api.create_profile(self.app.user, self.payload_investor_profile)
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
        profile = self.app.api.create_profile(self.app.user, self.payload_borrower_profile)
        self.assertNotEqual(None, profile)
        # self.window.profile_controller.setup_view()

        # Try to switch from borrower to investor
        user, _, _ = self.app.api.create_user()
        new_profile = self.app.api.create_profile(user, self.payload_investor_profile)
        self.app.user.role_id = 2
        self.window.profile_controller.update_form(new_profile)

        self.window.msg.about = MagicMock()
        QTest.mouseClick(self.window.profile_save_pushbutton, Qt.LeftButton)
        self.window.msg.about.assert_called_with(self.window, 'Profile saved', 'Your profile has been saved.')

    def test_profile_switch_role_invalid(self):
        # A user is only allowed to switch roles when he has no active loan requests or campaigns
        profile = self.app.api.create_profile(self.app.user, self.payload_borrower_profile)
        self.assertNotEqual(None, profile)
        # self.window.profile_controller.setup_view()

        # Place a loan request
        self.app.api.create_loan_request(self.app.user, self.payload_loan_request)
        # Try to switch from borrower to investor
        user, _, _ = self.app.api.create_user()
        new_profile = self.app.api.create_profile(user, self.payload_investor_profile)
        self.app.user.role_id = 2
        self.window.profile_controller.update_form(new_profile)

        self.window.msg.about = MagicMock()
        QTest.mouseClick(self.window.profile_save_pushbutton, Qt.LeftButton)
        self.window.msg.about.assert_called_with(self.window, 'Role switch failed',
                                                 'It is not possible to change your role at this time')

    def test_place_loan_request_empty(self):
        self.app.api.create_profile(self.app.user, self.payload_borrower_profile)

        self.window.msg.about = MagicMock()
        QTest.mouseClick(self.window.bplr_submit_pushbutton, Qt.LeftButton)
        self.window.msg.about.assert_called_with(self.window, 'Loan request error',
                                                 "You didn't enter the required information.")

    def test_place_loan_request_filled_in_linear(self):
        # Ui_MainWindow.bplr_bank1_checkbox.
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

    def test_place_loan_request_filled_in_fixed(self):
        # Ui_MainWindow.bplr_fixedrate_radiobutton
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
        # Ui_MainWindow.bplr_description_textedit.se
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
        # Ui_MainWindow.bplr_bank1_checkbox.
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
        QTest.mouseClick(self.window.bplr_submit_pushbutton, Qt.LeftButton)
        self.window.msg.about.assert_called_with(self.window, 'Loan request error', 'You can only have a single loan request.')

    def test_openmarket_no_select(self):
        self.window.openmarket_controller.setup_view()
        # print self.window.openmarket_controller.content[0][0].__dict__
        # self.assertFalse(self.window.openmarket_open_market_table.rowCount())

    def test_openmarket_table_filled(self):
        # Create the investor user
        role_id = Role.INVESTOR.value
        self.window.app.user.role_id = role_id
        self.window.api.db.put(User._type, self.window.app.user.id, self.window.app.user)

        # Create borrowers
        borrower1, _, _ = self.window.api.create_user()
        role_id = Role.BORROWER.value
        borrower1.role_id = role_id
        self.window.api.db.put(User._type, borrower1.id, borrower1)

        borrower2, _, _ = self.window.api.create_user()
        borrower2.role_id = role_id
        self.window.api.db.put(User._type, borrower2.id, borrower2)

        # Create loan requests
        borrower1 = self.window.api.db.get(User._type, borrower1.id)
        loan_request1 = self.window.api.create_loan_request(borrower1, self.payload_loan_request)

        borrower2 = self.window.api.db.get(User._type, borrower2.id)
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
        self.window.api.place_loan_offer(self.window.app.user, self.payload_loan_offer)

        self.payload_loan_offer['mortgage_id'] = mortgage2.id
        self.payload_loan_offer['amount'] = 123456
        loan_offer2 = self.window.api.place_loan_offer(self.window.app.user, self.payload_loan_offer)

        # Check if there's only 2 investments in the table
        self.window.openmarket_controller.setup_view()
        # self.assertEqual(self.window.ip_investments_table.rowCount(), 2)
        #
        # # Check if the first investment is in the table with the right values
        # self.assertEqual(self.window.ip_investments_table.item(0, 0).text(), 'straat 11, 1111AA')
        # self.assertEqual(self.window.ip_investments_table.item(0, 1).text(), 'Running')
        # self.assertEqual(self.window.ip_investments_table.item(0, 2).text(), 'Pending')
        # self.assertEqual(self.window.ip_investments_table.item(0, 3).text(), '1000')
        # self.assertEqual(self.window.ip_investments_table.item(0, 4).text(), '2.5')
        # self.assertEqual(self.window.ip_investments_table.item(0, 5).text(), '24')
        #
        # # Check if the second investment is in the table with the right values
        # self.assertEqual(self.window.ip_investments_table.item(1, 0).text(), 'straat 11, 1111AA')
        # self.assertEqual(self.window.ip_investments_table.item(1, 1).text(), 'Completed')
        # self.assertEqual(self.window.ip_investments_table.item(1, 3).text(), '123456')
        # self.assertEqual(self.window.ip_investments_table.item(1, 4).text(), '2.5')
        # self.assertEqual(self.window.ip_investments_table.item(1, 5).text(), '24')

    def test_openmarket_view_campaign_no_focus(self):
        self.window.msg.about = MagicMock()
        QTest.mouseClick(self.window.openmarket_view_loan_bids_pushbutton, Qt.LeftButton)
        self.window.msg.about.assert_called_with(self.window, "Select campaign", 'No campaigns have been selected.')

    def test_openmarket_view_campaign(self):
        # Create the investor user
        role_id = Role.INVESTOR.value
        self.window.app.user.role_id = role_id
        self.window.api.db.put(User._type, self.window.app.user.id, self.window.app.user)

        # Create borrowers
        borrower1, _, _ = self.window.api.create_user()
        role_id = Role.BORROWER.value
        borrower1.role_id = role_id
        self.window.api.db.put(User._type, borrower1.id, borrower1)

        # Create loan requests
        borrower1 = self.window.api.db.get(User._type, borrower1.id)
        loan_request1 = self.window.api.create_loan_request(borrower1, self.payload_loan_request)

        # Accept the loan requests
        self.payload_mortgage['user_key'] = borrower1.id
        self.payload_mortgage['request_id'] = loan_request1.id
        self.payload_mortgage['house_id'] = self.payload_loan_request['house_id']
        self.payload_mortgage['mortgage_type'] = self.payload_loan_request['mortgage_type']

        accepted_loan_request1, mortgage1 = self.window.api.accept_loan_request(self.window.app.bank1,
                                                                                self.payload_mortgage)

        # Accept mortgages
        self.window.api.accept_mortgage_offer(borrower1, {'mortgage_id': mortgage1.id})
        self.window.openmarket_controller.setup_view()
        self.window.openmarket_open_market_table.selectRow(0)

        print self.window.openmarket_open_market_table.selectedIndexes()
        self.window.msg.about = MagicMock()
        self.window.navigation.switch_to_campaign_bids = MagicMock()
        QTest.mouseClick(self.window.openmarket_view_loan_bids_pushbutton, Qt.LeftButton)
        # self.window.navigation.switch_to_campaign_bids.assert_called_with(mortgage1.id)

    def test_view_campaign_no_bids(self):
        # Create the investor user
        role_id = Role.INVESTOR.value
        self.window.app.user.role_id = role_id
        self.window.api.db.put(User._type, self.window.app.user.id, self.window.app.user)

        # Create borrowers
        borrower1, _, _ = self.window.api.create_user()
        role_id = Role.BORROWER.value
        borrower1.role_id = role_id
        self.window.api.db.put(User._type, borrower1.id, borrower1)

        borrower2, _, _ = self.window.api.create_user()
        borrower2.role_id = role_id
        self.window.api.db.put(User._type, borrower2.id, borrower2)

        # Create loan requests
        borrower1 = self.window.api.db.get(User._type, borrower1.id)
        loan_request1 = self.window.api.create_loan_request(borrower1, self.payload_loan_request)

        borrower2 = self.window.api.db.get(User._type, borrower2.id)
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
        self.window.api.place_loan_offer(self.window.app.user, self.payload_loan_offer)

        self.payload_loan_offer['mortgage_id'] = mortgage2.id
        self.payload_loan_offer['amount'] = 123456
        loan_offer2 = self.window.api.place_loan_offer(self.window.app.user, self.payload_loan_offer)

        # Accept one of the loan offers
        self.window.api.accept_investment_offer(borrower2, {'investment_id' : loan_offer2.id})

        # Check if there's only 2 investments in the table
        self.window.ip_controller.setup_view()
        self.assertEqual(self.window.ip_investments_table.rowCount(), 2)

    def test_navigation_initial_visibility(self):
        navigation = NavigateUser(self.window)
        self.assertFalse(navigation.mainwindow.navigation_pushbutton_1.isVisible())
        self.assertFalse(navigation.mainwindow.navigation_pushbutton_2.isVisible())
        self.assertFalse(navigation.mainwindow.navigation_pushbutton_3.isVisible())
        self.assertFalse(navigation.mainwindow.navigation_pushbutton_4.isVisible())

    def test_navigation_switching(self):
        navigation = NavigateUser(self.window)
        # self.window = Ui_MainWindow

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

    def test_navigation_user(self):
        self.app.user.role_id = 0
        self.window.navigation.switch_to_profile = MagicMock()
        self.window.navigation.user_screen_navigation()
        self.window.navigation.switch_to_profile.assert_called()
        self.app.user.role_id = 1
        self.window.navigation.set_borrower_navigation = MagicMock()
        self.window.navigation.user_screen_navigation()
        self.window.navigation.set_borrower_navigation.assert_called()
        self.app.user.role_id = 2
        self.window.navigation.set_investor_navigation = MagicMock()
        self.window.navigation.user_screen_navigation()
        self.window.navigation.set_investor_navigation.assert_called()
        self.app.user.role_id = 3
        self.window.navigation.set_bank_navigation = MagicMock()
        self.window.navigation.user_screen_navigation()
        self.window.navigation.set_bank_navigation.assert_called()

    def test_navigation_borrower(self):
        self.window.navigation.set_borrower_navigation()
        self.assertEqual('Profile', self.window.navigation_pushbutton_1.text())
        self.assertEqual('Portfolio', self.window.navigation_pushbutton_2.text())
        self.assertEqual('Place Loan Request', self.window.navigation_pushbutton_3.text())
        self.assertEqual('Open Market', self.window.navigation_pushbutton_4.text())

    def test_navigation_investor(self):
        self.window.navigation.set_investor_navigation()
        self.assertEqual('Profile', self.window.navigation_pushbutton_1.text())
        self.assertEqual('Portfolio', self.window.navigation_pushbutton_2.text())
        self.assertEqual('Open Market', self.window.navigation_pushbutton_3.text())

    def test_navigation_bank(self):
        self.window.navigation.set_bank_navigation()
        self.assertEqual('Portfolio', self.window.navigation_pushbutton_1.text())
        self.assertEqual('Loan Requests', self.window.navigation_pushbutton_2.text())
        self.assertEqual('Open Market', self.window.navigation_pushbutton_3.text())



###################################################################################################################

    def test_investors_portfolio_table_empty(self):
        # Check if the investments list is empty
        self.window.ip_controller.setup_view()
        self.assertFalse(self.window.ip_investments_table.rowCount())

    def test_investors_portfolio_table_filled(self):
        # Create the investor user
        role_id = Role.INVESTOR.value
        self.window.app.user.role_id = role_id
        self.window.api.db.put(User._type, self.window.app.user.id, self.window.app.user)

        # Create borrowers
        borrower1, _, _ = self.window.api.create_user()
        role_id = Role.BORROWER.value
        borrower1.role_id = role_id
        self.window.api.db.put(User._type, borrower1.id, borrower1)

        borrower2, _, _ = self.window.api.create_user()
        borrower2.role_id = role_id
        self.window.api.db.put(User._type, borrower2.id, borrower2)

        # Create loan requests
        borrower1 = self.window.api.db.get(User._type, borrower1.id)
        loan_request1 = self.window.api.create_loan_request(borrower1, self.payload_loan_request)

        borrower2 = self.window.api.db.get(User._type, borrower2.id)
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
        self.window.api.place_loan_offer(self.window.app.user, self.payload_loan_offer)

        self.payload_loan_offer['mortgage_id'] = mortgage2.id
        self.payload_loan_offer['amount'] = 123456
        loan_offer2 = self.window.api.place_loan_offer(self.window.app.user, self.payload_loan_offer)

        # Accept one of the loan offers
        self.window.api.accept_investment_offer(borrower2, {'investment_id' : loan_offer2.id})

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

        # Check if the second investment is in the table with the right values
        self.assertEqual(self.window.ip_investments_table.item(1, 0).text(), 'straat 11, 1111AA')
        self.assertEqual(self.window.ip_investments_table.item(1, 1).text(), 'Completed')
        self.assertEqual(self.window.ip_investments_table.item(1, 3).text(), '123456')
        self.assertEqual(self.window.ip_investments_table.item(1, 4).text(), '2.5')
        self.assertEqual(self.window.ip_investments_table.item(1, 5).text(), '24')

    def test_banks_portfolio_table_empty(self):
        # Check if the mortgage list is empty
        self.window.fip_controller.setup_view()
        self.assertFalse(self.window.fip_campaigns_table.rowCount())

    def test_banks_portfolio_table_filled(self):
        # Create the bank user
        self.window.app.user = self.window.app.bank1

        # Create borrowers
        borrower1, _, _ = self.window.api.create_user()
        role_id = Role.BORROWER.value
        borrower1.role_id = role_id
        self.window.api.db.put(User._type, borrower1.id, borrower1)

        borrower2, _, _ = self.window.api.create_user()
        borrower2.role_id = role_id
        self.window.api.db.put(User._type, borrower2.id, borrower2)

        # Create loan requests
        borrower1 = self.window.api.db.get(User._type, borrower1.id)
        loan_request1 = self.window.api.create_loan_request(borrower1, self.payload_loan_request)

        borrower2 = self.window.api.db.get(User._type, borrower2.id)
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
        self.window.api.db.put(User._type, investor.id, investor)

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

        # Check if the second mortgage is in the table with the right values
        self.assertEqual(self.window.fip_campaigns_table.item(1, 0).text(), 'straat 11, 1111AA')
        self.assertEqual(self.window.fip_campaigns_table.item(1, 1).text(), 'Running')
        self.assertEqual(self.window.fip_campaigns_table.item(1, 2).text(), '123000')
        self.assertEqual(self.window.fip_campaigns_table.item(1, 3).text(), '5.5')
        self.assertEqual(self.window.fip_campaigns_table.item(1, 4).text(), '9.0')
        self.assertEqual(self.window.fip_campaigns_table.item(1, 5).text(), '30')

    def test_pending_loan_requests_table_empty(self):
        # Check if the loan request list is empty
        self.window.fiplr1_controller.setup_view()
        self.assertFalse(self.window.fiplr1_loan_requests_table.rowCount())

    def test_pending_loan_requests_table_filled(self):
        # Create the bank user
        self.window.app.user = self.window.app.bank1

        # Create borrowers
        borrower1, _, _ = self.window.api.create_user()
        role_id = Role.BORROWER.value
        borrower1.role_id = role_id
        self.window.api.db.put(User._type, borrower1.id, borrower1)

        borrower2, _, _ = self.window.api.create_user()
        borrower2.role_id = role_id
        self.window.api.db.put(User._type, borrower2.id, borrower2)

        # Create loan requests
        borrower1 = self.window.api.db.get(User._type, borrower1.id)
        self.window.api.create_loan_request(borrower1, self.payload_loan_request)

        borrower2 = self.window.api.db.get(User._type, borrower2.id)
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
        # Click the 'view loan request' button without selecting an item in the table
        self.window.fiplr1_controller.setup_view()
        self.window.msg.about = MagicMock()
        QTest.mouseClick(self.window.fiplr1_view_loan_request_pushbutton, Qt.LeftButton)

        # Check if a dialog opens
        self.window.msg.about.assert_called_with(self.window, "Select request",
                                                 'No loan requests have been selected.')

    def test_pending_loan_requests_table_selected(self):
        # Create the bank user
        self.window.app.user = self.window.app.bank1

        # Create a borrower
        borrower, _, _ = self.window.api.create_user()
        role_id = Role.BORROWER.value
        borrower.role_id = role_id
        self.window.api.db.put(User._type, borrower.id, borrower)

        # Create a loan request
        borrower = self.window.api.db.get(User._type, borrower.id)
        loan_request = self.window.api.create_loan_request(borrower, self.payload_loan_request)

        # Select the item on the first row in the first column in the table
        self.window.fiplr1_controller.setup_view()
        self.window.fiplr1_loan_requests_table.selectRow(0)

        # Click the 'view loan request' button
        self.window.msg.about = MagicMock()
        self.window.fiplr2_controller.setup_view = MagicMock()
        QTest.mouseClick(self.window.fiplr1_view_loan_request_pushbutton, Qt.LeftButton)

        # Check if the 'pending loan request' view has been called
        self.window.fiplr2_controller.setup_view.assert_called_with(loan_request.id)

    def test_pending_loan_request_forms_filled_linear(self):
        # Create the bank user
        self.window.app.user = self.window.app.bank1

        # Create a borrower with profile
        borrower, _, _ = self.window.api.create_user()
        role_id = Role.BORROWER.value
        borrower.role_id = role_id
        self.window.api.db.put(User._type, borrower.id, borrower)
        self.window.api.create_profile(borrower, self.payload_borrower_profile)

        # Create a loan request
        borrower = self.window.api.db.get(User._type, borrower.id)
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
        # Create the bank user
        self.window.app.user = self.window.app.bank1

        # Create a borrower with profile
        borrower, _, _ = self.window.api.create_user()
        role_id = Role.BORROWER.value
        borrower.role_id = role_id
        self.window.api.db.put(User._type, borrower.id, borrower)
        self.window.api.create_profile(borrower, self.payload_borrower_profile)

        # Create a loan request
        borrower = self.window.api.db.get(User._type, borrower.id)
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
        # Create the bank user
        self.window.app.user = self.window.app.bank1

        # Create a borrower with profile
        borrower, _, _ = self.window.api.create_user()
        role_id = Role.BORROWER.value
        borrower.role_id = role_id
        self.window.api.db.put(User._type, borrower.id, borrower)
        self.window.api.create_profile(borrower, self.payload_borrower_profile)

        # Create a loan request
        borrower = self.window.api.db.get(User._type, borrower.id)
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
        # Create the bank user
        self.window.app.user = self.window.app.bank1

        # Create a borrower with profile
        borrower, _, _ = self.window.api.create_user()
        role_id = Role.BORROWER.value
        borrower.role_id = role_id
        self.window.api.db.put(User._type, borrower.id, borrower)
        self.window.api.create_profile(borrower, self.payload_borrower_profile)

        # Create a loan request
        borrower = self.window.api.db.get(User._type, borrower.id)
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
        # Create the bank user
        self.window.app.user = self.window.app.bank1

        # Create a borrower with profile
        borrower, _, _ = self.window.api.create_user()
        role_id = Role.BORROWER.value
        borrower.role_id = role_id
        self.window.api.db.put(User._type, borrower.id, borrower)
        self.window.api.create_profile(borrower, self.payload_borrower_profile)

        # Create a loan request
        borrower = self.window.api.db.get(User._type, borrower.id)
        self.payload_loan_request['mortgage_type'] = 2
        loan_request = self.window.api.create_loan_request(borrower, self.payload_loan_request)
        self.window.app.user = self.window.api.db.get(User._type, self.window.app.user.id)

        # Click the 'reject' button
        self.window.fiplr2_controller.setup_view(loan_request.id)
        self.window.msg.about = MagicMock()
        QTest.mouseClick(self.window.fiplr2_reject_pushbutton, Qt.LeftButton)

        # Check if a dialog opens
        self.window.msg.about.assert_called_with(self.window, "Request rejected",
                                                 'This loan request has been rejected.')
