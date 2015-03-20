#!/usr/bin/env python3

"""
Shows the growth of galaxies (starting at various masses) over time
"""

import helpers.schechter as hs
import helpers.data as data
import helpers.graph as graph
import matplotlib.pyplot as plt
import sys


if __name__ == "__main__":
  d = data.schechter()
  start, masses = [8 + 0.5*i for i in range(7)], []

  # For a variety of start masses
  # Find the number density at that mass at the highest Z (target)
  # Find the masses that have the same number density at all other Z 
  # (binary search through all number densities until we find one that = the target. return the mass)

  for start_mass in start:
    masses.append([start_mass])
    target = hs.param_dub_schechter(start_mass, d.double[0][-1]) # Just Z
    # target = hs.dub_schechter(start_mass, *d.double[0][:-1]) # Everything except Z

    for i in range(1, len(d.double)):
      masses[-1].append(hs.binary_search(target, d.double[i][-1]))

  info = {'xlabel': r'$\mathregular{redshift}$', 'ylabel': r'$\mathregular{log(M/M_\odot)}$', 'title': "Mass at constant number density over time", 'xlim': [0.35, 2.75], 'invert_xaxis': True}
  graph.line(masses, d.z_avg, info)
  graph.cut_line([2.75, 9.5],[0.35, 8])
  plt.show()
