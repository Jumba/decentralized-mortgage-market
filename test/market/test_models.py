from __future__ import absolute_import

import os
import unittest
import uuid

import sys

from market.api.api import MarketAPI
from market.database.backends import MemoryBackend
from market.database.database import MarketDatabase
from market.models import DatabaseModel
from market.models.document import Document
from market.models.user import User


class ModelTestSuite(unittest.TestCase):
    def setUp(self):
        self.db = MarketDatabase(MemoryBackend())
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

        pre_hash = model.generate_sha1_hash()
        # Sign the model
        model.sign(self.api)
        post_hash = model.generate_sha1_hash()

        self.assertEqual(pre_hash, post_hash)
        self.assertEqual(model.signer, self.db.backend.get_option('user_key_pub'))
        self.assertTrue(DatabaseModel.signature_valid(model))

    def test_signed_model_detect_tamper(self):
        """
        Test is models can be signed, and if the signature is read as valid
        """
        model = DatabaseModel()
        model.post_or_put(self.db)

        pre_hash = model.generate_sha1_hash()
        # Sign the model
        model.sign(self.api)

        #Tamper with the model
        model._id = 'different'

        post_hash = model.generate_sha1_hash()

        self.assertNotEqual(pre_hash, post_hash)
        self.assertEqual(model.signer, self.db.backend.get_option('user_key_pub'))
        self.assertFalse(DatabaseModel.signature_valid(model))


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

    def test_post_or_put_time(self):
        model = DatabaseModel()

        # Save the model, sign it, then save the signed version.
        model.post_or_put(self.db)
        model.sign(self.api)
        model.post_or_put(self.db)

        original_sign_time = model.time_signed

        # get a copy
        model_copy = self.db.get('database_model', model.id)

        self.assertEqual(original_sign_time, model_copy.time_signed)

        model_copy.sign(self.api)
        new_sign_time = model.time_signed
        model_copy.post_or_put(self.db)

        model_new_copy = self.db.get('database_model', model.id)
        self.assertEqual(new_sign_time, model_new_copy.time_signed)

        # Now we check that older models arent saved.
        model_new_copy._time_signed = 0
        model_new_copy.post_or_put(self.db, check_time=True)

        model_last_copy = self.db.get('database_model', model.id)
        self.assertEqual(new_sign_time, model_last_copy.time_signed)

    def test_user_key_immutable(self):
        """
        Test is an error is raised when attempting to change the user key.
        """
        public_key = 'pk'
        time_added = 100

        user = User(public_key, time_added)
        user.post_or_put(self.api.db)

        self.assertEqual(user.time_added, time_added)
        with self.assertRaises(IndexError) as cm:
            user.generate_id(force=True)

        exception = cm.exception
        self.assertEqual(exception.message, "User key is immutable")


    def test_document_model(self):
        file_name = 'test.py'
        mime = 'text/x-python'
        file_path = os.path.join(os.path.dirname(sys.modules['market'].__file__), '__init__.py')
        document = Document.encode_document(file_name, file_path)

        self.assertTrue(isinstance(document, Document))
        self.assertEqual(document.name, file_name)
        self.assertEqual(document.mime, mime)

        this_folder = os.getcwd()
        document.decode_document(os.path.join(this_folder, file_name))
        new_file_path = os.path.join(this_folder, file_name)

        self.assertEqual(open(file_path).read(), open(new_file_path).read())

        # Cleanup
        os.remove(new_file_path)

