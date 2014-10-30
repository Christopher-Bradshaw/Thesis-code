#!/usr/bin/python3

"""
Pick a start mass of galaxy (say 8)
Find the number density at highest Z of that mass
Find the mass with that number density at all other Z
graph the increase of mass as Z decreases
"""

""" TODO
paramaterization
"""
import helpers as h
import data
import graph
import matplotlib.pyplot as plt

# Given a min value, a max value, a target finds the value closest to the target after some number of iterations
# Target is a number density
# Returns the mass at that number density
def binary_search(start, stop, iters, target, z_params):
  for i in range(iters):
    guess = h.dub_schechter((start+stop)/2, *z_params)
    if guess < target:
      stop = (start + stop) / 2
    elif guess > target:
      start = (start + stop) / 2
    else: # Unlikely...
      return((start + stop) / 2)
  return((start + stop)/ 2)

if __name__ == "__main__":
  d = data.schechter()
  #start, masses = [8 + 0.1*i for i in range(31)], []
  start, masses = [8 + 0.5*i for i in range(7)], []

  for start_mass in start:
    masses.append([start_mass])
    # Find the number density of the start mass galaxies at the highest Z
    target = h.dub_schechter(start_mass, *d.double[0])

    for z_params in d.double[1:]:
      # Find the mass that at lower Z matches the target number density
      masses[-1].append(binary_search(6, 12, 100, target, z_params))

  info = {'xlabel': r'Z', 'ylabel': r'Mass', 'legend': d.z_range, 'title': "Mass at constant number density over time", 'xlim': [0.35, 2.75]}
  graph.line(masses, d.z_avg, info)
  graph.cut_line([2.75, 9.5],[0.35, 8])
  plt.show()
