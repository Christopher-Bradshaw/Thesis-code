#!/usr/bin/env python3

"""
Shows the growth of galaxies (starting at various masses) over time
"""

import helpers.schechter as h
import helpers.data as data
import helpers.graph as graph
import matplotlib.pyplot as plt
import sys

# Given a min value, a max value, a target finds the value closest to the target after some number of iterations
# Target is a number density
# Returns the mass at that number density
def binary_search(target, z, start=0, stop=0, iters=0):
  # Don't mess with these unless you have good reason
  start = start if start else 2
  stop = stop if stop else 12
  iters = iters if iters else 100

  for i in range(iters):
    guess = h.param_dub_schechter((start+stop)/2, z)
    # guess = h.dub_schechter((start+stop)/2, *z_params[:-1]) # when passing all params
    if guess < target:
      stop = (start + stop) / 2
    elif guess > target:
      start = (start + stop) / 2
    else: # Unlikely...
      return((start + stop) / 2)
  return((start + stop)/ 2)

# Given a start mass, start time (z0) and end time (z1)
# returns the growth (in m_sun) over that time based on the param_dub_schechter
def growth_over_time(m, z0, z1):
  target = h.param_dub_schechter(m, z0)
  m1 = binary_search(target, z1)
  return(m1)

if __name__ == "__main__":
  d = data.schechter()
  start, masses = [8 + 0.5*i for i in range(7)], []

  # For a variety of start masses
  # Find the number density at that mass at the highest Z (target)
  # Find the masses that have the same number density at all other Z 
  # (binary search through all number densities until we find one that = the target. return the mass)

  for start_mass in start:
    masses.append([start_mass])
    target = h.param_dub_schechter(start_mass, d.double[0][-1]) # Just Z
    # target = h.dub_schechter(start_mass, *d.double[0][:-1]) # Everything except Z

    for i in range(1, len(d.double)):
      masses[-1].append(binary_search(target, d.double[i][-1]))

  info = {'xlabel': r'$\mathregular{redshift}$', 'ylabel': r'$\mathregular{log(M/M_\odot)}$', 'title': "Mass at constant number density over time", 'xlim': [0.35, 2.75], 'invert_xaxis': True}
  graph.line(masses, d.z_avg, info)
  graph.cut_line([2.75, 9.5],[0.35, 8])
  plt.show()
