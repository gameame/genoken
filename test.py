import unittest
from genoken import Evolve

class TestEvolve(unittest.TestCase):
	def setUp(self):
		self.e = Evolve()
	def testcycle(self):
		self.e.cycle()

if __name__ == '__main__':
	unittest.main()
