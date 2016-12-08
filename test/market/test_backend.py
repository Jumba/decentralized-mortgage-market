import unittest

from market.database.backends import Backend, MemoryBackend, PersistentBackend
from market.models import DatabaseModel


class BackendTestSuite(unittest.TestCase):
    def setUp(self):
        self.backend = Backend()

    def test_get(self):
        with self.assertRaises(NotImplementedError):
            self.backend.get(None, None)

    def test_put(self):
        with self.assertRaises(NotImplementedError):
            self.backend.put(None, None, None)

    def test_post(self):
        with self.assertRaises(NotImplementedError):
            self.backend.post(None, None, None)

    def test_delete(self):
        with self.assertRaises(NotImplementedError):
            self.backend.delete(None)

    def test_id_check(self):
        with self.assertRaises(NotImplementedError):
            self.backend.id_available(None)

    def test_exists(self):
        with self.assertRaises(NotImplementedError):
            self.backend.exists(None, None)

    def test_get_all(self):
        with self.assertRaises(NotImplementedError):
            self.backend.get_all(None)


class MemoryBackendTestSuite(unittest.TestCase):
    def setUp(self):
        self.backend = MemoryBackend()


        class T(object):
            def __init__(self, id):
                self.id = id

        # Create some data
        self.block1 = T('1')
        self.block2 = T('2')
        self.block3 = T('3')

    def test_clear(self):
        self.backend.clear()
        self.backend.post('test', self.block1.id, self.block1)
        self.backend.clear()
        with self.assertRaises(IndexError):
            self.backend.get('test', self.block1.id)


    def test_post(self):
        self.backend.clear()
        self.backend.post('test', self.block1.id, self.block1)
        self.assertEqual(self.block1, self.backend.get('test', self.block1.id))

    def test_get(self):
        self.backend.clear()
        self.backend.post('test', self.block1.id,  self.block1)
        self.backend.post('test', self.block2.id, self.block2)
        self.backend.post('test', self.block3.id, self.block3)

        with self.assertRaises(IndexError):
            self.backend.post('test2', self.block1.id, self.block1)

        self.assertEqual(self.backend.get('test', '1'), self.block1)
        self.assertEqual(self.backend.get('test', self.block2.id), self.block2)
        self.assertNotEqual(self.backend.get('test', '1'), self.backend.get('test', '2'))

        with self.assertRaises(IndexError):
            self.assertEqual(self.backend.get('test', '1'), self.backend.get('test2', '1'))

    def test_get_error(self):
        self.backend.clear()
        with self.assertRaises(IndexError):
            self.backend.get('test', 1)

    def test_put_fail(self):
        self.backend.clear()
        self.assertFalse(self.backend.put('test', '1', self.block1))

    def test_put_success(self):
        self.backend.clear()
        self.backend.post('test', self.block1.id, self.block1)
        self.assertEqual(self.backend.get('test', self.block1.id), self.block1)

        self.assertTrue(self.backend.put('test', self.block1.id, self.block2))
        self.assertEqual(self.backend.get('test', self.block1.id), self.block2)


    def test_delete(self):
        self.backend.clear()
        with self.assertRaises(NotImplementedError):
            self.backend.delete(self.block1.id)

    def test_get_all(self):
        self.backend.clear()
        self.backend.post('test', self.block1.id, self.block1)
        self.backend.post('test', self.block2.id, self.block2)
        self.backend.post('boe', self.block3.id, self.block3)

        all_tests = self.backend.get_all('test')
        self.assertIsInstance(all_tests, list)
        self.assertIn(self.block1, all_tests)
        self.assertIn(self.block2, all_tests)
        self.assertNotIn(self.block3, all_tests)


class PersistentBackendTestSuite(unittest.TestCase):
    def setUp(self):
        self.backend = PersistentBackend('.')

        # Create some data
        self.block1 = DatabaseModel('1')
        self.block2 = DatabaseModel('2')
        self.block3 = DatabaseModel('3')

    def tearDown(self):
        self.backend.close()

    def test_clear(self):
        self.backend.clear()
        self.backend.post('test', self.block1.id, self.block1)
        self.backend.clear()
        with self.assertRaises(IndexError):
            self.backend.get('test', self.block1.id)

    def test_post(self):
        self.backend.clear()
        self.backend.post('test', self.block1.id, self.block1.encode())
        self.assertEqual(self.block1, DatabaseModel.decode(self.backend.get('test', self.block1.id)))

    def test_get(self):
        self.backend.clear()
        self.backend.post('test', self.block1.id,  self.block1.encode())
        self.backend.post('test', self.block2.id, self.block2.encode())
        self.backend.post('test', self.block3.id, self.block3.encode())

        with self.assertRaises(IndexError):
            self.backend.post('test2', self.block1.id, self.block1.encode())

        self.assertEqual(DatabaseModel.decode(self.backend.get('test', '1')), self.block1)
        self.assertEqual(DatabaseModel.decode(self.backend.get('test', self.block2.id)), self.block2)
        self.assertNotEqual(DatabaseModel.decode(self.backend.get('test', '1')), DatabaseModel.decode(self.backend.get('test', '2')))

        with self.assertRaises(IndexError):
            self.assertEqual(DatabaseModel.decode(self.backend.get('test', '1')), DatabaseModel.decode(self.backend.get('test2', '1')))

    def test_get_error(self):
        self.backend.clear()
        with self.assertRaises(IndexError):
            self.backend.get('test', 1)

    def test_put_fail(self):
        self.backend.clear()
        self.assertFalse(self.backend.put('test', '1', self.block1))

    def test_put_success(self):
        self.backend.clear()
        self.backend.post('test', self.block1.id, self.block1.encode())
        self.assertEqual(DatabaseModel.decode(self.backend.get('test', self.block1.id)), self.block1)

        self.assertTrue(self.backend.put('test', self.block1.id, self.block2.encode()))
        self.assertEqual(DatabaseModel.decode(self.backend.get('test', self.block1.id)), self.block2)

    def test_delete(self):
        self.backend.clear()
        self.backend.post('test', self.block1.id, self.block1)
        self.backend.delete(self.block1.id)

        self.assertFalse(self.backend.exists('test', self.block1.id))

    def test_get_all(self):
        self.backend.clear()
        self.backend.post('test', self.block1.id, self.block1.encode())
        self.backend.post('test', self.block2.id, self.block2.encode())
        self.backend.post('boe', self.block3.id, self.block3.encode())

        all_tests = self.backend.get_all('test')
        self.assertIsInstance(all_tests, list)
        self.assertIn(self.block1.encode(), all_tests)
        self.assertIn(self.block2.encode(), all_tests)
        self.assertNotIn(self.block3.encode(), all_tests)


if __name__ == '__main__':
    unittest.main()
