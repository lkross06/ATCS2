import unittest
from gcf_correct import func

class TestGCF(unittest.TestCase):
    def test_gcf(self):
        self.assertAlmostEqual(func(4, -6), 2)
        self.assertAlmostEqual(func(-6, 4), 2)
        self.assertAlmostEqual(func(0, 5), 0)
    
    def test_values(self):
        self.assertRaises(ValueError, func, 0, 0)