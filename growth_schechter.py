#!/usr/bin/python3

"""
Pick a start mass of galaxy (say 8)
Find the number density at highest Z of that mass
Find the mass with that number density at all other Z
graph the increase of mass as Z decreases
"""

import helpers.schechter as h
import helpers.data
import helpers.graph
import matplotlib.pyplot as plt
import sys

# Given a min value, a max value, a target finds the value closest to the target after some number of iterations
# Target is a number density
# Returns the mass at that number density
def binary_search(start, stop, iters, target, z_params):
  for i in range(iters):
    # guess = h.dub_schechter((start+stop)/2, *z_params)
    guess = h.param_dub_schechter((start+stop)/2, z_params[1], z_params[3], z_params[-1])
    if guess < target:
      stop = (start + stop) / 2
    elif guess > target:
      start = (start + stop) / 2
    else: # Unlikely...
      return((start + stop) / 2)
  return((start + stop)/ 2)

if __name__ == "__main__":
  d = data.schechter()
  start, masses = [8 + 0.5*i for i in range(7)], []

  # For a number of start masses
  # Find the number density at that start mass at the highest Z
  # Find the mass at that number density for all other Z
  for start_mass in start:
    masses.append([start_mass])
    # target = h.dub_schechter(start_mass, *d.double[0])
    target = h.param_dub_schechter(start_mass, d.double[0][1], d.double[0][3], d.double[0][-1])

    for i in range(1, len(d.double)):
      masses[-1].append(binary_search(6, 12, 10, target, d.double[i]))

  info = {'xlabel': r'$\mathregular{redshift}$', 'ylabel': r'$\mathregular{log(M/M_\odot)}$', 'title': "Mass at constant number density over time", 'xlim': [0.35, 2.75], 'invert_xaxis': True}
  graph.line(masses, d.z_avg, info)
  graph.cut_line([2.75, 9.5],[0.35, 8])
  plt.show()
