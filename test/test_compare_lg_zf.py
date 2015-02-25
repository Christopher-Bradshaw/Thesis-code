#!/usr/bin/env python
import unittest
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import compare_lg_zf as clz
import helpers.data as data

class Test_abs_masses_calc(unittest.TestCase):

  def setUp(self):
    self.sfh = data.sfh()

  def test_simple(self):
    self.sfh.total_mass = [1]
    self.sfh.total_mass_unc = [ [0.1, 0.2] ]
    self.sfh.mass = [ [0.1, 0.5, 1] ]
    self.sfh.mass_unc = [ [[0.2, 0.1], [0.3, 0.3], [0.5, 0.7]] ]

    exp_abs_masses = [[5.0, 5.698970004336019, 6.0]]
    exp_abs_masses_unc = [[5.301572186310091, 5.0], [5.483070866369516, 5.5], [5.707486673985409, 5.862137934800394]]

    abs_masses, abs_masses_unc = self.sfh.abs_mass()

    self.assertEqual(abs_masses, exp_abs_masses)


if __name__ == "__main__":
  unittest.main(verbosity=3)
