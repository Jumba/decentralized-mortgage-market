import unittest

from market.api.api import MarketAPI
from market.database.backends import MemoryBackend
from market.database.database import MockDatabase
from market.dispersy.crypto import ECCrypto
from market.models.profiles import BorrowersProfile
from market.models.profiles import Profile
from market.models.user import User


class APITestSuite(unittest.TestCase):
    def setUp(self):
        self.database = MockDatabase(MemoryBackend())
        self.api = MarketAPI(self.database)
        self.ec = ECCrypto()

        self.payload = {'role': 1, 'first_name': 'Bob', 'last_name': 'Saget', 'email': 'example@example.com', 'iban': 'NL53 INGBB 04027 30393', 'phonenumber': '+3170253719234',
                        'current_postalcode': '2162CD', 'current_housenumber': '22', 'documents_list': []}

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
