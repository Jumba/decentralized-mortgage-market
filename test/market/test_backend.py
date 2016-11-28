import unittest

from market.database.backends import Backend, MemoryBackend


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


if __name__ == '__main__':
    unittest.main()
