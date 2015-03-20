import unittest
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import helpers.whitaker as wh

class Test_whitaker_helpers(unittest.TestCase):
  def test_weight_params_works(self):
    data = [
        [[1.3, 1.1],  [0.99, 0.51, 1.31], 'both in a single partition'],
        [[1.3, 0.7],  [0.965, 0.325, 1.21], 'equally divided over two partitions'],
        [[1.1, 0.7],  [0.9525, 0.2325, 1.16], 'unequally divided over two partitions'],
        [[1.6, 0.9],  [0.99, 0.4729, 1.307], 'unequally divided over three partitions'],
        [[1.5, 1.0],  [0.99, 0.51, 1.31], 'boundaries conditions']
    ]
    for i in data:
      with self.subTest(i=i):
        res = wh.weight_parameters(*i[0])
        for j in range(3):
          self.assertAlmostEqual(res[j], i[1][j], places = 3)

  def test_weight_params_fails(self):
    data = [
        [[3.1, 1.1], 'z0 > 3'],
        [[1.1, 0.4], 'z1 < 0.5'],
        [[1.1, 1.4], 'z1 > z0']
    ]
    for i in data:
      with self.subTest(i=i) and self.assertRaises(RuntimeError, msg = i[1]):
        wh.weight_parameters(*i[0])

if __name__ == "__main__":
  unittest.main(verbosity=2)
