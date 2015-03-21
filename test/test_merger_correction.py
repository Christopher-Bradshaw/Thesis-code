import unittest
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import helpers.merger_correction as hmc
import math
import helpers.graph as graph
import matplotlib.pyplot as plt
from helpers.z_to_t import *

class Test_merger_corr(unittest.TestCase):

  def test_merger_correction(self):
    # The expected values were taken from illustris 2 graphs on pg 10
    data = [ #[m, u0, u1, z]
        [[1e8, 1/4, 0.1], 1.5e-2],
        [[1e10, 1/100, 0.1], 2.6],
        [[1e11, 1/1000, 1], 700],
        [[1e9, 1/10, 2], 1.5],
    ]
    for i in data:
      with self.subTest(i=i):
        self.assertAlmostEqual(hmc.merger_correction(*i[0]), i[1], delta=i[1]/10)

  def test_integrated_u_merger_correction(self):
    # The expected values were taken from illustris 2 graphs on pg 11
    data = [ #[m, u0, u1, z]
        [[1e8, 1/4, 1, 0.1], 5e-3],
        [[1e11, 1/100, 1, 1], 7e-1],
        [[1e9, 1/10, 1, 2], 2.5e-1],
        [[1e10, 1/4, 1, 0.1], 1.3e-2],
        [[1e10, 1/4, 1, 1], 6e-2],
    ]
    for i in data:
      with self.subTest(i=i):
        self.assertAlmostEqual(hmc.integrated_u_merger_correction(*i[0]), i[1], delta=i[1]/10)

  def test_integrated_uz_merger_correction(self):
    s = 1000
    data = [
        [[1e10, 1/4, 1, z_from_t(t_from_z(1) + 1/s), 1], self.assertGreater, hmc.integrated_u_merger_correction(1e10, 1/4, 1, 1)/s],
        [[1e10, 1/4, 1, 1, z_from_t(t_from_z(1) - 1/s)], self.assertLess, hmc.integrated_u_merger_correction(1e10, 1/4, 1, 1)/s],
    ]

    for i in data:
      with self.subTest(i=i):
        i[1](hmc.integrated_uz_merger_correction(*i[0]), i[2])

# This should generate graphs == to the top 3 on page 11 of the illustris paper
def integrated_u_merger_graphs():
  step, min_u = 10, [1/i for i in [4, 10, 100, 1000]]
  starts = [8, 8.2, 9.3, 10.3]
  mass = [[10**(i/step) for i in range(int(j*step), int(12.3*step))] for j in starts]
  for z in [0.1, 1, 2]:
    mergers = []
    for k, u in enumerate(min_u):
      mergers.append([])
      for i in mass[k]:
        mergers[-1].append(hmc.integrated_u_merger_correction(i, u, 1, z))
    graph.line(mergers, x=mass, info={'xlog': True, 'ylog': True, 'ylim': [3e-3, 2e1], 'xlim': [6e7, 2e12]})
  plt.show()

# This should generate graphs == to the second 3 on page 11 of the illustris paper
def integrated_u_merger_graphs2():
  step, mass = 20, [1e9, 1e10, 1e11]
  mass_ratio = [10**(i/step) for i in range(-4*step, 0)]
  for z in [0.1, 1, 2]:
    mergers = []
    for m in mass:
      mergers.append([])
      for u in mass_ratio:
        mergers[-1].append(hmc.integrated_u_merger_correction(m, u, 1, z))
    graph.line(mergers, x=mass_ratio, info={'xlog': True, 'ylog': True, 'ylim': [6e-4, 2e1], 'xlim': [1e-4, 1]})
  plt.show()

# This should generate graphs == to the top 3 on page 10 of the illustris paper
def merger_graphs():
  step, min_u = 10, [1/i for i in [4, 10, 100, 1000]]
  starts = [8, 8.6, 9.6, 10.6]
  mass = [[10**(i/step) for i in range(int(j*step), int(12.3*step))] for j in starts]
  for z in [0.1, 1, 2]:
    mergers = []
    for k, u in enumerate(min_u):
      mergers.append([])
      for i in mass[k]:
        mergers[-1].append(hmc.merger_correction(i, u, z))
    graph.line(mergers, x=mass, info={'xlog': True, 'ylog': True, 'ylim': [1e-2, 1e4], 'xlim': [6e7, 2e12]})
  plt.show()

# This should generate graphs == to the second 3 on page 10 of the illustris paper
def merger_graphs2():
  step, mass = 20, [1e9, 1e10, 1e11]
  mass_ratio = [10**(i/step) for i in range(-4*step, 0)]
  for z in [0.1, 1, 2]:
    mergers = []
    for m in mass:
      mergers.append([])
      for u in mass_ratio:
        mergers[-1].append(hmc.merger_correction(m, u, z))
    graph.line(mergers, x=mass_ratio, info={'xlog': True, 'ylog': True, 'ylim': [2e-3, 1e5], 'xlim': [1e-4, 1]})
  plt.show()

if __name__ == "__main__":
  if 0 and input('do you want graphs? (y/n)') == 'y':
    integrated_u_merger_graphs()
    integrated_u_merger_graphs2()
    merger_graphs()
    merger_graphs2()
  unittest.main(verbosity=2)
