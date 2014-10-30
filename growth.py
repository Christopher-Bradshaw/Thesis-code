#!/usr/bin/python3

"""
Pick a start mass of galaxy (say 8)
Find the number density at highest Z of that mass
Find the mass with that number density at all other Z
graph the increase of mass as Z decreases
"""


import helpers as h
import data
import graph
import matplotlib.pyplot as plt

# Given a min value, a max value, a target finds the value closest to the target after some number of iterations
# Target is a number density
# Returns the mass at that number density
def binary_search(target, z_params):
  iters = 10
  start = 6
  stop = 12
  for i in range(iters):
    guess = h.dub_schechter((start+stop)/2, *z_params)
    if guess < target:
      stop = (start + stop) / 2
    else:
      start = (start + stop) / 2
  return(guess, (start + stop)/ 2)



if __name__ == "__main__":
  # Paramtaters for double schechter
  d = data.schechter()
  s = d.double
  r = [i/100 for i in range(750, 1200)]


  start = [8, 8.5, 9, 9.5, 10, 10.5, 11]
  dens = []
  masses = []

  for start_mass in start:
    masses.append([start_mass])
    dens.append([h.dub_schechter(start_mass, *s[0])])

    for z_params in s[1:]:
      den, mass = binary_search(dens[-1][-1], z_params)
      dens[-1].append(den)
      masses[-1].append(mass)

  graph.line(masses, d.z_avg)
  plt.show()
