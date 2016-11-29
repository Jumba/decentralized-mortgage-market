import unittest
loader = unittest.TestLoader()
start_dir = 'test/market'
suite = loader.discover(start_dir, '*.py')

runner = unittest.TextTestRunner()
runner.run(suite)
