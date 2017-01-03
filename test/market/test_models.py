from __future__ import absolute_import
import unittest
import uuid

from market.api.api import MarketAPI
from market.database.backends import MemoryBackend
from market.database.database import MockDatabase
from market.models import DatabaseModel


class ModelTestSuite(unittest.TestCase):
    def setUp(self):
        self.db = MockDatabase(MemoryBackend())
        self.api = MarketAPI(self.db)

        self.db.backend.set_option('user_key_pub', "3081a7301006072a8648ce3d020106052b810400270381920004040a3d5712482be45375958745cdd3134ff079303bcf0ecf02ff6dff5b49cfde221a4068f1a243e31ba36052ed4836c77df8c1729cb9875ed703b23ccc9488f0b81ddba6e51b1caa01bc4e4c0152554c38b805ae6d9fb9d0a20172266b814a4f20e5ced5eb8f657c521b76dc6c10eb695444d69db8426a39232bd3e166eb22bcb7704642ca26a276774dc13d249b9e29")
        self.db.backend.set_option('user_key_priv', "3081ee0201010448017a656efdf1a6203fee24074e8e9aba1c329563321bbb17ddc069fccee0b9b5e5b505f4ac2131760b82cfb56301cac7a00341c812b7ae6b4867910c5ac8d4c23152ccaf64ba7956a00706052b81040027a181950381920004040a3d5712482be45375958745cdd3134ff079303bcf0ecf02ff6dff5b49cfde221a4068f1a243e31ba36052ed4836c77df8c1729cb9875ed703b23ccc9488f0b81ddba6e51b1caa01bc4e4c0152554c38b805ae6d9fb9d0a20172266b814a4f20e5ced5eb8f657c521b76dc6c10eb695444d69db8426a39232bd3e166eb22bcb7704642ca26a276774dc13d249b9e29")

    def test_signed_model_no_save(self):
        """
        Test if signing an unsaved model raises an error.
        """
        model = DatabaseModel()

        with self.assertRaises(RuntimeError):
            model.sign(self.api)

    def test_signed_model(self):
        """
        Test is models can be signed, and if the signature is read as valid
        """
        model = DatabaseModel()
        model.post_or_put(self.db)

        pre_hash = model._generate_sha1_hash()
        # Sign the model
        model.sign(self.api)
        post_hash = model._generate_sha1_hash()

        self.assertEqual(pre_hash, post_hash)
        self.assertEqual(model.signer, self.db.backend.get_option('user_key_pub'))
        self.assertTrue(model.signature_valid())

    def test_signed_model_detect_tamper(self):
        """
        Test is models can be signed, and if the signature is read as valid
        """
        model = DatabaseModel()
        model.post_or_put(self.db)

        pre_hash = model._generate_sha1_hash()
        # Sign the model
        model.sign(self.api)

        #Tamper with the model
        model._id = 'different'

        post_hash = model._generate_sha1_hash()

        self.assertNotEqual(pre_hash, post_hash)
        self.assertEqual(model.signer, self.db.backend.get_option('user_key_pub'))
        self.assertFalse(model.signature_valid())


    def test_model_equal(self):
        """
        Test if identical models have the same hash and are eveluated as equal
        """
        model1 = DatabaseModel()
        model2 = DatabaseModel()

        #self.assertEqual(hash(model1), hash(model2))
        self.assertEqual(model1, model2)

    def test_model_unequal(self):
        """
        Test if different models have different hashes and are evaluated as unequal
        """
        model1 = DatabaseModel()
        model2 = DatabaseModel()

        # Change the models by saving one and giving it an id
        model2.post_or_put(self.db)

        self.assertNotEqual(hash(model1), hash(model2))
        self.assertNotEqual(model1, model2)