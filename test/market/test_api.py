import unittest

from market.api.api import MarketAPI
from market.database.backends import MemoryBackend
from market.database.database import MockDatabase
from market.dispersy.crypto import ECCrypto
from market.models.user import User
from market.models.profiles import Profile
from market.models.profiles import BorrowersProfile


class APITestSuite(unittest.TestCase):
    def setUp(self):
        self.database = MockDatabase(MemoryBackend())
        self.api = MarketAPI(self.database)
        self.ec = ECCrypto()

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

    def test_create_profile(self):
        # Create an user
        user, pub, priv = self.api.create_user()

        # Create profile
        investors_profile = self.api.create_profile(user)
        borrowers_profile = self.api.create_profile(user)

        # Check if the Profile object is returned
        self.assertIsInstance(investors_profile, Profile)
        # Check if the BorrowersProfile object is returned
        self.assertIsInstance(borrowers_profile, BorrowersProfile)