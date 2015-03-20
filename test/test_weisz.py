import unittest
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import helpers.data as data
import helpers.weisz as wh


class Test_weisz_helpers(unittest.TestCase):
  @classmethod
  def setUpClass(self):
    self.g_exp = {'L': 0.4, 'G': 0.2, 'A': 0.4} # not real - makes testing easier

  def test_g_actual_bins(self):
    data = [
        [ [[[1, 2], 'G']], {'G': 1, 'A': 0, 'L': 0} ],
        [ [[[1, 2], 'G'], [[1, 2], 'A']], {'G': 0.5, 'A': 0.5, 'L': 0} ],
        [ [[[1, 2], 'G'], [[1, 2], 'A'], [[1, 2], 'G']], {'G': 2/3, 'A': 1/3, 'L': 0} ],
        [ [[[1, 2], 'G'], [[1, 2], 'A'], [[1, 2], 'G'], [[1, 2], 'L']], {'G': 0.5, 'A': 0.25, 'L': 0.25} ],
        [ [], {'A': 0, 'G': 0, 'L': 0} ]
    ]
    for i in data:
      self.assertEqual(wh.g_actual_bins(i[0]), i[1])

  def test_average_growth_rate(self):
    data = [
        [ [[[100, 200], 'G']], 100, 'simple'],
        [ [[[100, 200], 'G'], [[150, 200], 'G']], 75, 'expected freqs make no diff when only one g type'],
        [ [[[100, 200], 'A'], [[150, 200], 'L']], 75, 'expected freqs make no diff when gs of same prob'],
        [ [[[100, 200], 'A'], [[150, 200], 'G']], 250/3, 'expected freqs correct bin when acutal != exp'],
        [ [], 0, 'empty']
    ]
    for i in data:
      g_actual = wh.g_actual_bins(i[0])
      self.assertAlmostEqual(wh.average_growth_rate(self.g_exp, g_actual, i[0], 1, 0), i[1], msg = i[2])
      self.assertAlmostEqual(wh.average_growth_rate(self.g_exp, g_actual, i[0], 2, 0), i[1]/2, msg = i[2])

  # Not 100% comfortable with these corrections, but they seem to work
  def test_bin_uncertainty(self):
    data = [
        [ [[[[100, 100], [100, 100]], 'G']], [141.42, 141.42], 'simple'],
        [ [[[[100, 100], [100, 200]], 'G']], [141.42, 223.61], 'simple 2'],
        [ [[[[100, 100], [100, 100]], 'L'], [[[100, 100], [100, 100]], 'L']], [100, 100], 'simple 3'],
        [ [[[[200, 200], [100, 100]], 'L'], [[[200, 100], [100, 100]], 'L']], [158.11, 132.29], 'simple 4'],
        [ [[[[200, 200], [100, 100]], 'L'], [[[200, 100], [100, 100]], 'A']], [158.11, 132.29], 'weigh makes no difference if equal'],
        [ [[[[100, 100], [100, 100]], 'L'] for i in range(4)] + [[[[100, 100], [100, 100]], 'G']], [66.67, 66.67], 'one correction'],
        [ [[[[100, 100], [100, 100]], 'L'], [[[100, 100], [100, 100]], 'G']], [105.41, 105.41], 'two corrections'],
        [ [], [0, 0], 'empty']
    ]
    for i in data:
      g_actual = wh.g_actual_bins(i[0])
      for j in [1, 2]:
        res = wh.bin_uncertainty(self.g_exp, g_actual, i[0], j, 0)
        self.assertAlmostEqual(res[0], i[1][0]/j, msg = i[2], places = 2)
        self.assertAlmostEqual(res[1], i[1][1]/j, msg = i[2], places = 2)

  def test_average_bin_start(self):
    data = [
        [ [[[100, 888], 'G']], 2, 'simple'],
        [ [[[80, 777], 'G'], [[120, 444], 'G']], 2, 'expected freqs make no diff when only one g type'],
        [ [[[80, 999], 'A'], [[120, 555], 'L']], 2, 'expected freqs make no diff when gs of same prob'],
        [ [[[100, 333], 'A'], [[150, 111], 'G']], 2.07, 'expected freqs correct bin when acutal != exp'],
        [ [], 0, 'empty']
    ]
    for i in data:
      g_actual = wh.g_actual_bins(i[0])
      self.assertAlmostEqual(wh.average_bin_start(self.g_exp, g_actual, i[0]), i[1], msg = i[2], places = 2)

  def test_uncertainty_bin_start(self):
    data = [
        [ [[[[100, 200], [777, 888]], 'G']], 3, [0.0414, 0.0969], 'simple'],
        [ [[[[100, 200], [777, 888]], 'G']], 4, [0.0043, 0.0088], 'simple'],
        [ [[[[100, 100], [100, 100]], 'L'] for i in range(4)] + [[[[100, 100], [100, 100]], 'G']], 3, [0.0200, 0.0210], 'one correction'],
        [ [[[[100, 100], [100, 100]], 'L'], [[[100, 100], [100, 100]], 'G']], 2, [0.2419, 0.5941], 'two corrections'],
        [ [], 3, [0, 0], 'empty']
    ]
    for i in data:
      g_actual = wh.g_actual_bins(i[0])
      res = wh.uncertainty_bin_start(self.g_exp, g_actual, i[0], i[1])
      self.assertAlmostEqual(res[0], i[2][0], msg = i[3], places = 4)
      self.assertAlmostEqual(res[1], i[2][1], msg = i[3], places = 4)
