#!/usr/bin/env python3
import unittest
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import helpers.data as data
import helpers.z_to_t as z_to_t

# Add test for non 50% abs_masses case
class Test_sfh_data(unittest.TestCase):
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


  def test_lengths(self):
    self.assertTrue(len(self.sfh.names) == len(self.sfh.g_loc) == len(self.sfh.g_type) == len(self.sfh.total_mass) == len(self.sfh.total_mass_unc) == len(self.sfh.mass) == len(self.sfh.mass_unc))
    for i in self.sfh.mass:
      self.assertEqual(len(i), len(self.sfh.mass[0]))
    for i in self.sfh.mass_unc:
      self.assertEqual(len(i), len(self.sfh.mass[0])) # not a typo

  def test_abs_times(self):
    times = [round(z_to_t.z_from_t(10 ** i / 10 ** 9), 5) for i in self.sfh.legend[:2]] # just do the first 2 to make this faster
    self.assertEqual(times, self.sfh.z_times[:2])

  def test_get_loc(self):
    locs = self.sfh.get_loc()
    g_loc = ['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'G', 'L', 'G', 'G', 'L', 'G', 'G', 'G', 'A', 'L', 'L', 'L', 'L', 'G', 'G', 'G', 'L', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'L', 'L', 'L', 'L','L', 'L', 'L', 'G', 'G', 'G', 'G', 'L', 'L', 'L', 'L', 'G', 'L', 'L']
    self.assertEqual(g_loc, locs)

  def test_g_actual(self):
    percs = self.sfh.g_actual()
    self.assertEqual(percs['G'], 0.2641509433962264)
    self.assertEqual(percs['A'], 0.3584905660377358)
    self.assertEqual(percs['L'], 0.37735849056603776)

  def test_expected_percs(self):
    percs = self.sfh.g_exp
    self.assertEqual(percs['G'], 0.27)
    self.assertEqual(percs['A'], 0.33)
    self.assertEqual(percs['L'], 0.40)


if __name__ == "__main__":
  unittest.main(verbosity=3)
