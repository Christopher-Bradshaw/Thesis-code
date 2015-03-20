import unittest
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import helpers.schechter as hs
import math

class Test_schechter_functions(unittest.TestCase):

  def test_schechter(self):
    data = [ #[m, m_star, a, phi]
        [7, 11.35,  -1.74, -4.36],
        [8, 11.13,  -1.43, -3.59],
        [9, 11.03,  -1.33, -3.28]
    ]
    for i in data:
      with self.subTest(i=i):
        # Taken from zfourge paper. phi is given as log10(phi). Output of schechter function is log10
        expected = math.log10(math.log(10) * 10**i[3] * 10 ** ((i[0] - i[1]) * (1+i[2])) * math.e ** (-10**(i[0] - i[1])))
        self.assertAlmostEqual(hs.schechter(*i), expected)

  def test_double_schechter(self):
    data = [ #[m, m_star, a1, phi1, a2, phi2]
        [7, 10.74,  1.62, -4.54, -1.57, -3.69],
        [8, 10.69,  1.03, -3.80, -1.33, -3.26],
        [9, 10.74,  0.04, -3.05, -1.49, -3.38]
    ]
    for i in data:
      with self.subTest(i=i):
        # Taken from zfourge paper. phi is given as log10(phi). Output of schechter function is log10
        _ = math.log(10) * math.e ** (-10 ** (i[0] - i[1])) * 10 ** (i[0] - i[1])
        expected = _ * (10 ** i[3] * 10 ** ((i[0] - i[1])*i[2]) + 10 ** i[5] * 10 ** ((i[0] - i[1]) * i[4]))
        self.assertAlmostEqual(hs.double_schechter(*i), math.log10(expected))

  def test_param_double_schecter(self):
    data = [ #[m, z]
        [1, 1], [2,10], [0.4, 17], [12, 0]
    ]
    a1, a2 = -0.39, -1.53

    for i in data:
      with self.subTest(i=i):
        phi1 = -2.46 + 0.07*i[1] - 0.28*i[1]**2
        phi2 = -3.11 - 0.18*i[1] - 0.03*i[1]**2
        ms = 10.72 - 0.13*i[1] + 0.11*i[1]**2
        _ = math.log(10) * math.e ** (-10 ** (i[0] - ms)) * 10 ** (i[0] - ms)
        expected = _ * (10 ** phi1 * 10 ** ((i[0] - ms)*a1) + 10 ** phi2 * 10 ** ((i[0] - ms) * a2))
        self.assertAlmostEqual(hs.param_double_schechter(*i), math.log10(expected))




if __name__ == "__main__":
  unittest.main(verbosity=2)
