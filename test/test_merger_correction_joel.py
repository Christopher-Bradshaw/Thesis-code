# Check whether my method and Joel's agree

import unittest
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import helpers.merger_correction as hmc
import math
import helpers.graph as graph
import matplotlib.pyplot as plt
from helpers.z_to_t import *


# Returns the percentage of galaxies that disappear between z0 and z1 at various masses
def percent_dead(z0):
  z1 = z_from_t(t_from_z(2) - 0.1)
  print(z0, z1)

  corr, x, uncorr = hmc.correct_smf(z0, z1)
  print(corr, x, uncorr)
  data = [1 - uncorr[i]/corr[i] for i in range(len(corr))]
  graph.line([data], x, info={'ylog':True})
  graph.line([corr, uncorr], x, info={'ylog':True})
  plt.show()

if __name__ == '__main__':
  percent_dead(2)

