#!/usr/bin/env python3
import unittest
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import compare_lg_zf as clz
import helpers.data as data

class Test_sfh(unittest.TestCase):

  def setUp(self):
    self.sfh = data.sfh()

  def test_abs_masses(self):
    self.sfh.total_mass = [1] # in units of 1e6
    self.sfh.total_mass_unc = [ [0.1, 0.2] ]
    self.sfh.mass = [ [0.1, 0.5, 1] ]
    self.sfh.mass_unc = [ [[0.2, 0.1], [0.3, 0.3], [0.5, 0.7]] ]

    exp_abs_masses = [[64000, 320000, 640000]]
    exp_abs_masses_unc = [[[32000, 32000], [160000, 160000], [320000, 320000]]]

    abs_masses, abs_masses_unc = self.sfh.abs_mass()

    self.assertEqual(abs_masses, exp_abs_masses)
    self.assertEqual(abs_masses_unc, exp_abs_masses_unc)

  def test_abs_times(self):
    times = self.sfh.abs_times()
    self.assertEqual(times, self.sfh.z_times)


if __name__ == "__main__":
  unittest.main(verbosity=3)
