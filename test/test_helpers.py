#!/usr/bin/env python3
import unittest
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import helpers.z_to_t as z_to_t
import helpers.helpers as h


class Test_helpers(unittest.TestCase):

  def test_z_and_t_works(self):
    z_times = [3,2,1]
    res = h.z_and_t_from_index_t_step(0, 1, z_times)
    self.assertEqual(res[0], 3)
    self.assertEqual(res[2], 2)

  def test_z_and_t_fails(self):
    z_times = [3,2,1]
    with self.assertRaises(IndexError, msg = 't_step was too great'):
      h.z_and_t_from_index_t_step(0, 3, z_times)
    self.assertRaises(AssertionError, h.z_and_t_from_index_t_step, 0, -1, z_times)

  def test_find_nearest(self):
    val, vals = 1, [0.3, 0.9, 0.7, 1.2]
    self.assertEqual(h.find_nearest(vals, val), 1)

    val, vals = 1, [0.3, 0.9, 0.7, 1.1]
    self.assertEqual(h.find_nearest(vals, val), 1)

  def test_bins_centers(self):
    data = [
        [[2, 0, 1], [0.25, 0.75]],
        [[50, 0, 1], [0.01 + 0.02*i for i in range(50)]],
        [[1, 0, 1], [0.5]],
    ]

    for i in data:
      with self.subTest(i=i):
        self.assertEqual(h.bins_centers(*i[0]), i[1])


if __name__ == "__main__":
  unittest.main(verbosity=2)
