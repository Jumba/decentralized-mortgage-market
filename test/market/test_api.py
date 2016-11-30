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
        self.payload1 = {'role': 1, 'user_key': 'rfghiw98594pio3rjfkhs', 'amount': 1000, 'duration': 24, 'interest_rate': 2.5,
                         'mortgage_id': '8739-a875ru-hd938-9384', 'status': 'pending'}

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
        self.payload1['role'] = 2  # investor
        profile = self.api.create_profile(user, self.payload)

        # Create loan offer
        self.payload1['user_key'] = user.id # set user_key to the investor's public key
        loan_offer = self.api.place_loan_offer(user, self.payload1)

        # Check if the Profile object is returned
        self.assertIsInstance(profile, Profile)
        # Check if the Investment object is returned
        self.assertIsInstance(loan_offer, Investment)
        # Check if the investment id is saved in the user's investment ids list
        self.assertEqual(user.investment_ids[-1], loan_offer.id)

    def test_place_loan_offer_borrower(self):
        # Create an user
        user, pub, priv = self.api.create_user()

        # Create an borrower profile
        self.payload['role'] = 1  # borrower
        self.payload1['role'] = 1 # borrower
        profile = self.api.create_profile(user, self.payload)

        # Create loan offer
        self.payload1['user_key'] = user.id  # set user_key to the borrower's public key
        loan_offer = self.api.place_loan_offer(user, self.payload1)

        # Check if the Profile object is returned
        self.assertIsInstance(profile, Profile)
        # Check if the Investment object is returned
        self.assertFalse(loan_offer)
        # Check if the investment ids list is empty
        self.assertEquals(user.investment_ids, [])

    def test_place_loan_offer_bank(self):
        # Create an user
        user, pub, priv = self.api.create_user()

        # Create an borrower profile
        self.payload['role'] = 3  # bank
        self.payload1['role'] = 3 # bank
        profile = self.api.create_profile(user, self.payload)

        # Create loan offer
        self.payload1['user_key'] = user.id  # set user_key to the bank's public key
        loan_offer = self.api.place_loan_offer(user, self.payload1)

        # Check if the Profile object is returned
        self.assertFalse(profile)
        # Check if the Investment object is returned
        self.assertFalse(loan_offer)
        # Check if the investment ids list is empty
        self.assertEquals(user.investment_ids, [])

    def test_accept_loan_request(self):
        # create a user
        user, pub, priv = self.api.create_user()
        self.payload['role'] = 3  # bank

        self.payload['loan_request_id'] = 1
        loan_request, mortgage = self.api.accept_loan_request(user, self.payload)

        assert isinstance(loan_request, LoanRequest)
        assert isinstance(mortgage, Mortgage)
        self.assertEquals(loan_request.status, 'ACCEPTED')

    def test_reject_loan_request(self):
        self.payload['loan_request_id'] = 1

        loan_request = self.api.reject_loan_request(self.payload)
        assert isinstance(loan_request, LoanRequest)

        print loan_request.status
        self.assertEquals(loan_request.status, 3)