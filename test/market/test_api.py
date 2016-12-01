import unittest

from market.api.api import MarketAPI
from market.database.backends import MemoryBackend
from market.database.database import MockDatabase
from market.dispersy.crypto import ECCrypto
from market.models.loans import LoanRequest, Mortgage
from market.models.profiles import BorrowersProfile
from market.models.profiles import Profile
from market.models.user import User
from market.models.loans import Investment


class APITestSuite(unittest.TestCase):
    def setUp(self):
        self.database = MockDatabase(MemoryBackend())
        self.api = MarketAPI(self.database)
        self.ec = ECCrypto()

        self.payload = {'role': 1, 'first_name': 'Bob', 'last_name': 'Saget', 'email': 'example@example.com', 'iban': 'NL53 INGBB 04027 30393', 'phonenumber': '+3170253719234',
                        'current_postalcode': '2162CD', 'current_housenumber': '22', 'documents_list': []}
        self.payload_loan_offer1 = {'role': 1, 'user_key': 'rfghiw98594pio3rjfkhs', 'amount': 1000, 'duration': 24, 'interest_rate': 2.5,
                         'mortgage_id': '8739-a875ru-hd938-9384', 'status': 'pending'}
        self.payload_loan_offer2 = {'role': 1, 'user_key': 'rfghiw93iuedij3565534', 'amount': 20000, 'duration': 36, 'interest_rate': 3.5,
                         'mortgage_id': '8jd39-a875ru-h09ru8-9384', 'status': 'accepted'}
        self.payload_loan_offer3 = {'role': 1, 'user_key': 'r98iw98594p09eikhs', 'amount': 500, 'duration': 12, 'interest_rate': 7.0,
                         'mortgage_id': '3757-a876u-h1m38-dm83', 'status': 'rejected'}
        self.payload_loan_request = {'role': 0, 'user_key': 'rfghiw98594pio3rjfkhs',
                                     'house_id': '8739-a875ru-hd938-9384', 'mortgage_type': 1, 'banks': [],
                                     'description': unicode('I want to buy a house'), 'amount_wanted': 123456,
                                     'status': {'bank1': 'none', 'bank2': 'none', 'bank3': 'none', 'bank4': 'none'}}

    def test_create_user(self):
        user, pub, priv = self.api.create_user()

        # Check if the user object is returned
        self.assertIsInstance(user, User)

        # Check if the public and private keys are valid
        self.assertTrue(self.ec.is_valid_public_bin(pub.decode("HEX")))
        self.assertTrue(self.ec.is_valid_private_bin(priv.decode("HEX")))

    def test_login_user(self):
        # Create an user
        user, pub, priv = self.api.create_user()

        # Login the user using his private key
        user_login = self.api.login_user(priv)

        # Confirm is the user returned is equal to the user created.
        self.assertEqual(user, user_login)

    def test_create_borrower_profile(self):
        # Create an user
        user, pub, priv = self.api.create_user()

        # Create a borrowers profile
        self.payload['role'] = 1  # borrower
        profile = self.api.create_profile(user, self.payload)

        # Check if the BorrowersProfile object is returned
        self.assertIsInstance(profile, BorrowersProfile)

        # Check if the profile id is saved in the user.
        self.assertEqual(user.profile_id, profile.id)

    def test_create_investor_profile(self):
        # Create an user
        user, pub, priv = self.api.create_user()

        # Create an investors profile
        self.payload['role'] = 2  # investor
        profile = self.api.create_profile(user, self.payload)

        # Check if the Profile object is returned
        self.assertIsInstance(profile, Profile)

        # Check if the profile id is saved in the user.
        self.assertEqual(user.profile_id, profile.id)

    def test_create_bank_profile(self):
        # Create an user
        user, pub, priv = self.api.create_user()

        # Create a bank profile
        self.payload['role'] = 3  # bank
        profile = self.api.create_profile(user, self.payload)

        # Check if the Profile object is returned
        self.assertFalse(profile)

        # Check if the profile id is empty in the user
        self.assertIsNone(user.profile_id)

    def test_create_profile_keyerror(self):
        # Create an user
        user, pub, priv = self.api.create_user()

        # Delete an essential key in the payload
        del self.payload['role']
        profile = self.api.create_profile(user, self.payload)

        # Check if the Profile object is returned
        self.assertFalse(profile)

    def test_load_profile_borrower(self):
        # Create an user
        user, pub, priv = self.api.create_user()

        # Create a borrowers profile
        self.payload['role'] = 1  # borrower
        profile = self.api.create_profile(user, self.payload)

        # Get the profile
        loaded_profile = self.api.load_profile(user)

        # Check if the returned profile is the profile in the database
        self.assertEqual(profile, loaded_profile)
        self.assertIsInstance(profile, BorrowersProfile)

    def test_load_profile_investor(self):
        # Create an user
        user, pub, priv = self.api.create_user()

        # Create a borrowers profile
        self.payload['role'] = 2  # investor
        profile = self.api.create_profile(user, self.payload)

        # Get the profile
        loaded_profile = self.api.load_profile(user)

        # Check if the returned profile is the profile in the database
        self.assertEqual(profile, loaded_profile)
        self.assertIsInstance(profile, Profile)

    def test_load_profile_bank(self):
        # Create an user
        user, pub, priv = self.api.create_user()

        # Create a bank profile
        self.payload['role'] = 3  # bank
        profile = self.api.create_profile(user, self.payload)
        # Get the profile
        loaded_profile = self.api.load_profile(user)

        # Check if the Profile object is returned
        self.assertFalse(profile)
        self.assertFalse(loaded_profile)
        # Check if the profile id is empty in the user
        self.assertIsNone(user.profile_id)

    def test_place_loan_offer_investor(self):
        # Create an user
        user, pub, priv = self.api.create_user()

        # Create an investor profile
        self.payload['role'] = 2  # investor
        self.payload_loan_offer1['role'] = 2  # investor
        self.payload_loan_offer2['role'] = 2  # investor
        profile = self.api.create_profile(user, self.payload)

        # Create loan offer
        self.payload_loan_offer1['user_key'] = user.id # set user_key to the investor's public key
        self.payload_loan_offer2['user_key'] = user.id  # set user_key to the investor's public key
        loan_offer = self.api.place_loan_offer(user, self.payload_loan_offer1)
        loan_offer2 = self.api.place_loan_offer(user, self.payload_loan_offer2)

        # Check if the Profile object is returned
        self.assertIsInstance(profile, Profile)
        # Check if the Investment object is returned
        self.assertIsInstance(loan_offer, Investment)
        self.assertIsInstance(loan_offer2, Investment)

        # Check if the investments have separate id.
        self.assertNotEqual(loan_offer, loan_offer2)

        # Check if the investment ids are saved in the user's investment ids list
        self.assertIn(loan_offer.id, user.investment_ids)
        self.assertIn(loan_offer2.id, user.investment_ids)


    def test_place_loan_offer_borrower(self):
        # Create an user
        user, pub, priv = self.api.create_user()

        # Create an borrower profile
        self.payload['role'] = 1  # borrower
        self.payload_loan_offer1['role'] = 1 # borrower
        profile = self.api.create_profile(user, self.payload)

        # Create loan offer
        self.payload_loan_offer1['user_key'] = user.id  # set user_key to the borrower's public key
        loan_offer = self.api.place_loan_offer(user, self.payload_loan_offer1)

        # Check if the Profile object is returned
        self.assertIsInstance(profile, Profile)
        # Check if the Investment object is returned
        self.assertFalse(loan_offer)
        # Check if the investment ids list is empty
        self.assertEqual(user.investment_ids, [])

    def test_place_loan_offer_bank(self):
        # Create an user
        user, pub, priv = self.api.create_user()

        # Create an borrower profile
        self.payload['role'] = 3  # bank
        self.payload_loan_offer1['role'] = 3 # bank
        profile = self.api.create_profile(user, self.payload)

        # Create loan offer
        self.payload_loan_offer1['user_key'] = user.id  # set user_key to the bank's public key
        loan_offer = self.api.place_loan_offer(user, self.payload_loan_offer1)

        # Check if the Profile object is returned
        self.assertFalse(profile)
        # Check if the Investment object is returned
        self.assertFalse(loan_offer)
        # Check if the investment ids list is empty
        self.assertEqual(user.investment_ids, [])

    #def test_create_loan_request_borrower(self):
        # Create a user

    def test_load_investments(self):
        # Create an user
        user, pub, priv = self.api.create_user()

        # Create an investor's profile
        self.payload['role'] = 2  # investor
        self.payload_loan_offer1['role'] = 2  # investor
        self.payload_loan_offer2['role'] = 2  # investor
        self.payload_loan_offer3['role'] = 2  # investor
        profile = self.api.create_profile(user, self.payload)

        # Create loan offers
        self.payload_loan_offer1['user_key'] = user.id  # set user_key to the investor's public key
        self.payload_loan_offer2['user_key'] = user.id  # set user_key to the investor's public key
        self.payload_loan_offer3['user_key'] = user.id  # set user_key to the investor's public key
        loan_offer1 = self.api.place_loan_offer(user, self.payload_loan_offer1)
        loan_offer2 = self.api.place_loan_offer(user, self.payload_loan_offer2)
        loan_offer3 = self.api.place_loan_offer(user, self.payload_loan_offer3)

        # Get the investments
        current_investment, pending_investment = self.api.load_investments(user)

        # Check if the returned objects are Lists
        self.assertIsInstance(current_investment, list)
        self.assertIsInstance(pending_investment, list)
        # Check if the elements of the lists are Investment-objects
        for investment in current_investment:
            self.assertIsInstance(investment, Investment)
        for investment in pending_investment:
            self.assertIsInstance(investment, Investment)
        # Check if the Investment-objects are saved in the correct list
        self.assertIn(loan_offer1, pending_investment)
        self.assertIn(loan_offer2, current_investment)
        self.assertNotIn(loan_offer3, pending_investment)
        self.assertNotIn(loan_offer3, current_investment)

    def test_check_role_borrower(self):
        # create a user
        user, pub, priv = self.api.create_user()

        # Create a borrower profile
        self.payload['role'] = 1  # borrower
        self.api.create_profile(user, self.payload)

        # Get the role of the user
        role = self.api.check_role(user)

        # Check whether the returned role is indeed the user's role
        self.assertEqual(role.id, user.role_id)
        self.assertEqual(role.role_name, "BORROWER")

    def test_check_role_investor(self):
        # create a user
        user, pub, priv = self.api.create_user()

        # Create a borrower profile
        self.payload['role'] = 2  # investor
        self.api.create_profile(user, self.payload)

        # Get the role of the user
        role = self.api.check_role(user)

        # Check whether the returned role is indeed the user's role
        self.assertEqual(role.id, user.role_id)
        self.assertEqual(role.role_name, "INVESTOR")

    def test_check_role_bank(self):
        # create a user
        user, pub, priv = self.api.create_user()

        # Create a borrower profile
        self.payload['role'] = 3  # bank/financial institution
        self.api.create_profile(user, self.payload)

        # Get the role of the user
        role = self.api.check_role(user)

        # Check whether the returned role is indeed the user's role
        self.assertEqual(role.id, user.role_id)
        self.assertEqual(role.role_name, "FINANCIAL_INSTITUTION")

    def test_create_loan_request_borrower(self):
        # create a user
        user, pub, priv = self.api.create_user()

        # Create a borrower profile
        self.payload['role'] = 1  # borrower
        self.payload_loan_request['role'] = 1  # borrower
        profile = self.api.create_profile(user, self.payload)

        # Create loan request
        self.payload['user_key'] = user.id  # set user_key to the borrower's public key
        loan_request = self.api.create_loan_request(user, self.payload_loan_request)

        # Check if the Profile object is returned
        self.assertIsInstance(profile, Profile)
        # Check if the LoanRequest object is returned
        self.assertIsInstance(loan_request, LoanRequest)
        # Check if the loan request id is saved in the user's loan_request_id
        self.assertEqual(user.loan_request_id, loan_request.id)
        # Check if the status is set to pending
        for bank in self.payload_loan_request['status']:
            self.assertEqual(self.payload_loan_request['status'][bank], 'pending')

    def test_create_loan_request_investor(self):
        # Create a user
        user, pub, priv = self.api.create_user()

        # Create a investor profile
        self.payload['role'] = 2  # investor
        self.payload_loan_request['role'] = 2  # investor
        profile = self.api.create_profile(user, self.payload)

        # Create loan request
        self.payload['user_key'] = user.id  # set user_key to the borrower's public key
        loan_request = self.api.create_loan_request(user, self.payload_loan_request)

        # Check if the Profile object is returned
        self.assertIsInstance(profile, Profile)
        # Check if the LoanRequest object is returned
        self.assertFalse(loan_request)
        # Check if the loan_request_id is empty
        self.assertEquals(user.loan_request_id, None)
        # Check if the status is not set to pending
        for bank in self.payload_loan_request['status']:
            self.assertEquals(self.payload_loan_request['status'][bank], 'none')

    def test_create_loan_request_bank(self):
        # Create a user
        user, pub, priv = self.api.create_user()

        # Create a bank profile
        self.payload['role'] = 3  # bank
        self.payload_loan_request['role'] = 3  # bank
        profile = self.api.create_profile(user, self.payload)

        # Create loan request
        self.payload['user_key'] = user.id  # set user_key to the borrower's public key
        loan_request = self.api.create_loan_request(user, self.payload_loan_request)

        # Check if the Profile object is returned
        self.assertFalse(profile)
        # Check if the LoanRequest object is returned
        self.assertFalse(loan_request)
        # Check if the loan_request_id is empty
        self.assertEquals(user.loan_request_id, None)
        # Check if the status is not set to pending
        for bank in self.payload_loan_request['status']:
            self.assertEquals(self.payload_loan_request['status'][bank], 'none')


            #    def test_accept_loan_request(self):
#        # create a user
#        user, pub, priv = self.api.create_user()
#        self.payload['role'] = 3  # bank

#        self.payload['loan_request_id'] = 1
#        loan_request, mortgage = self.api.accept_loan_request(user, self.payload)

#        assert isinstance(loan_request, LoanRequest)
#        assert isinstance(mortgage, Mortgage)
#        self.assertEquals(loan_request.status, 'ACCEPTED')

#    def test_reject_loan_request(self):
#        self.payload['loan_request_id'] = 1

#        loan_request = self.api.reject_loan_request(self.payload)
#        assert isinstance(loan_request, LoanRequest)

#        self.assertEquals(loan_request.status, 3)
