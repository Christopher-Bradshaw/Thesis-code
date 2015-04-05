#!/usr/bin/env python3

'''
Finds the best approximation to the slow z_to_t formula
'''
from os import path
import sys
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import math
import helpers.z_to_t as z_to_t
import matplotlib.pyplot as plt
import helpers.graph as graph

if __name__ == '__main__':
  zs = [i/10 for i in range(31)]
  res = [[],[]]
  for z in zs:
    res[0].append(z_to_t.old_t_from_z(z))
    res[1].append(z_to_t.t_from_z(z))
  graph.line(res, x=zs)

  ts = res[0]
  res = [[], []]
  for t in ts:
    res[0].append(z_to_t.old_z_from_t(t))
    res[1].append(z_to_t.z_from_t(t))

  graph.line(res, x=ts)
  plt.show()
