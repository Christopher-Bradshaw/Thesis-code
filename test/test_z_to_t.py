import unittest
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import helpers.z_to_t as z_to_t

class Test_merger_corr(unittest.TestCase):

  # Given a z, returns the TIME AGO in Gyr
  def test_z_to_t(self):
    data = [
        [0, 0],
        [1, 7.817],
        [2, 10.404],
        [17, 13.493],
    ]
    for i in data:
      with self.subTest(i=i):
        self.assertAlmostEqual(z_to_t.t_from_z(i[0]), i[1], places=3)

  # Given a TIME AGO in Gyr, returns the z
  def test_z_from_t(self):
    data = [
        [0, 0],
        [7.817, 1],
        [10.404, 2],
    ]
    for i in data:
      with self.subTest(i=i):
        self.assertAlmostEqual(z_to_t.z_from_t(i[0]), i[1], places=3)

  # Because we binary search, we specify max z = 6 (to increase resolution below that.
  # Report error if z >= 6
  def test_z_to_t_fails(self):
    data = [13.493, 12.779]
    for i in data:
      with self.subTest(i=i) and self.assertRaises(Exception, msg='Too long ago = change stop time of seach'):
        z_to_t.z_from_t(i)


if __name__ == "__main__":
  unittest.main(verbosity=2)
