from __future__ import absolute_import
import unittest

from market.database.backends import MemoryBackend, PersistentBackend
from market.database.database import Database, MarketDatabase
from market.models import DatabaseModel


class DatabaseTestSuite(unittest.TestCase):
    def setUp(self):
        self.database = Database()

    def test_get(self):
        with self.assertRaises(NotImplementedError):
            self.database.get(None, None)

    def test_put(self):
        with self.assertRaises(NotImplementedError):
            self.database.put(None, None, None)

    def test_post(self):
        with self.assertRaises(NotImplementedError):
            self.database.post(None, None)

    def test_delete(self):
        with self.assertRaises(NotImplementedError):
            self.database.delete(None, None)

    def test_get_all(self):
        with self.assertRaises(NotImplementedError):
            self.database.get_all(None)


class DatabaseTestSuite(unittest.TestCase):
    def setUp(self):
        self.database = MarketDatabase(MemoryBackend())

        # Some database models
        self.model1 = DatabaseModel()
        self.model2 = DatabaseModel()

    def test_init(self):
        database = MarketDatabase(MemoryBackend())

        # Raise an error if no backend is given
        with self.assertRaises(AssertionError):
            database2 = MarketDatabase(None)

    def test_post(self):
        # Check if it has no id prior to saving
        self.assertIsNone(self.model1.id)

        id = self.database.post(self.model1.type, self.model1)

        # Check if id saved to model
        self.assertEqual(self.model1.id, self.database.get(self.model1.type, self.model1.id).id)

    def test_get(self):
        self.database.post(self.model1.type, self.model1)

        # Get the same object
        self.assertEqual(self.model1, self.database.get(self.model1.type, self.model1.id))

        # Get a noneexisting model
        self.assertIsNone(self.database.get(self.model1.type, 'invalid_id'))

    def test_put(self):
        # Put an unsaved model
        with self.assertRaises(AssertionError):
            self.assertFalse(self.database.put(self.model1.type, self.model1.id, self.model1))

        # Fake an id
        self.model1._id = "fake"

        # Replace a nonexisting element
        self.assertFalse(self.database.put(self.model1.type, self.model1.id, self.model1))

        # Replace an existing element correctly
        test_string = "boo"
        with self.assertRaises(AttributeError):
            self.assertEqual(self.model1.test, test_string)

        self.model1.test = test_string
        self.database.post(self.model1.type, self.model1)

        # Check if the test string was saved in the db
        self.assertEqual(self.database.get(self.model1.type, self.model1.id).test, test_string)

        # Change the string
        test_string2 = "baa"
        self.model1.test = test_string2
        self.assertTrue(self.database.put(self.model1.type, self.model1.id, self.model1))
        self.assertEqual(self.database.get(self.model1.type, self.model1.id).test, test_string2)

        # Finally check if we can't replace it with another id
        self.model2._id = "not_id_of_model1"
        with self.assertRaises(AssertionError):
            self.assertFalse(self.database.put(self.model1.type, self.model1.id, self.model2))

    def test_delete_assert(self):
        with self.assertRaises(AssertionError):
            self.database.delete(None)

    def test_delete(self):
        self.database.post(self.model1.type, self.model1)
        self.assertTrue(self.database.delete(self.model1))
        self.assertIsNone(self.database.get(self.model1.type, self.model1.id))



    def test_get_all(self):
        self.database.post(self.model1.type, self.model1)
        self.database.post(self.model2.type, self.model2)
        # Get the same object
        all_tests = self.database.get_all(self.model1.type)
        self.assertIsInstance(all_tests, list)
        self.assertIn(self.model1, self.database.get_all(self.model1.type))
        self.assertIn(self.model2, self.database.get_all(self.model2.type))

        # Get a noneexisting model
        self.assertIsNone(self.database.get_all('hi'))


class DatabasePersistentTestSuite(DatabaseTestSuite):
    def setUp(self):
        self.database = MarketDatabase(PersistentBackend('.'))
        self.database.backend.clear()
        # Some database models
        self.model1 = DatabaseModel()
        self.model2 = DatabaseModel()

    def tearDown(self):
        self.database.backend.close()

