import unittest
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import helpers.z_to_t as z_to_t
import helpers.graph as graph
import matplotlib.pyplot as plt
import time

class Test_merger_corr(unittest.TestCase):

  # Given a z, returns the TIME AGO in Gyr
  def test_t_from_z(self):
    data = [
        [0, 0],
        [1, 7.860],
        [2, 10.480],
        [3, 11.559],
    ]
    for i in data:
      with self.subTest(i=i):
        self.assertAlmostEqual(z_to_t.t_from_z(i[0]), i[1], places=3)

  # Given a TIME AGO in Gyr, returns the z
  # 0.2s
  def test_z_from_t(self):
    data = [
        [0, 0],
        [7.817, 0.99],
        [10.404, 1.953],
    ]
    for i in data:
      with self.subTest(i=i):
        self.assertAlmostEqual(z_to_t.z_from_t(i[0]), i[1], places=3)

  # Because we binary search, we specify max z = 3 (to increase resolution below that.
  def test_z_from_t_fails(self):
    data = [13.493, 12.779]
    for i in data:
      with self.subTest(i=i) and self.assertRaises(Exception, msg='T too high!'):
        z_to_t.z_from_t(i)

  # Because we binary search, we specify max z = 3 (to increase resolution below that.
  def test_t_from_z_fails(self):
    data = [3.1, 10000]
    for i in data:
      with self.subTest(i=i) and self.assertRaises(Exception, msg='Z too high!'):
        z_to_t.t_from_z(i)
def z_graphs():
  step = 10
  x = [i/step for i in range(30)]
  y = [z_to_t.t_from_z(i) for i in x]
  graph.line([y], x=x, info={'ylabel': 'Time (Gyr)', 'xlabel': 'Z', 'title': 'Lookback Time vs Redshift'})
  plt.show()

if __name__ == "__main__":
  if 1 and input('do you want graphs? (y/n)') == 'y':
    z_graphs()
  unittest.main(verbosity=2)
