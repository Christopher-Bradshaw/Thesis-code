#!/usr/bin/env python3

import math
import sys
import graph
import z_to_t
import matplotlib.pyplot as plt

# Input is exactly the same as data.schechter.single (except for no z) and required m
def schechter(m, ms, a, phi_s):
  phi_s = 10 ** phi_s
  ret = math.log(10) * phi_s * (10 ** ((m - ms) * (1 + a))) * (math.e ** (-10 ** (m - ms)))
  return(math.log10(ret))


# Input is exactly the same as data.schechter.double (except for no z) and required m
def dub_schechter(m, ms, a1, phi_s1, a2, phi_s2):
  phi_s1 = 10 ** phi_s1
  phi_s2 = 10 ** phi_s2

  a = math.log(10) * math.e ** (-10 ** (m - ms)) * 10 ** (m - ms)
  b = phi_s1 * 10 ** ((m - ms) * a1) + phi_s2 * 10 ** ((m - ms) * a2)
  return(math.log10(a * b))

def param_dub_schechter(m, z):
  a1 = -0.39
  a2 = -1.53
  phi_s1 = 10 ** (-2.46 + 0.07*z - 0.28*z*z)
  phi_s2 = 10 ** (-3.11 - 0.18*z - 0.03*z*z)
  ms = 10.72 - 0.13*z + 0.11*z*z

  a = math.log(10) * math.e ** (-10 ** (m - ms)) * 10 ** (m - ms)
  b = phi_s1 * 10 ** ((m - ms) * a1) + phi_s2 * 10 ** ((m - ms) * a2)
  return(math.log10(a * b))


# Numbers of mergers per Gyr at specified start mass, ratio and redshift
def merger_correction(M, u, z):

  A0, n, a0, a1, b0, b1, y, g0, g1, M0 = 10**(-2.2287), 2.4644, 0.2241, -1.1759, -1.2595, 0.0611, -0.0477, 0.7668, 0.4695, 2e11


  A_z = A0*(1+z)**n
  a_z = a0*(1+z)**a1
  b_z = b0*(1+z)**b1
  g_z = g0*(1+z)**g1
  a_z = a0*(1+z)**a1

  res = A_z * (M/1e10)**a_z * (1 + (M/M0)**g_z) * u ** (b_z + y * math.log10(M/1e10))
  return(res)

# Integrates the merger corr between z1 and z0 for all u
# The chance that any galaxy at this mass undergoes a merger
# So, if 0.5 multiply SMF at new z by 0.5
#     if 0.1 multiply SMF at new z by 0.9 -> (1-res)
def integrated_merger_corr(M, z0, z1):
  u_depth, u, us = 10, 1, [] # u to go until, starting u, array of mergers percs for u
  z_bins = 20 # number of bins to split z_diff into
  z_diff = (z0 - z1)/z_bins

  while u < u_depth:
    u1, tmp_res = u + u/10, 0
    us.append([(u+u1)/2])

    for i in range(z_bins):
      z = z0 + (z_diff * (i+0.5))
      t_diff = z_to_t.t_from_z(z + z_diff) - z_to_t.t_from_z(z)
      a = merger_correction(M, (u1+u)/2, z)
      if a < 0:
        sys.exit()
      tmp_res += merger_correction(M, (u1+u)/2, z) * t_diff * (u1-u)

    us[-1].append(tmp_res)
    u = u1

  #res = sum([i[1] for i in us])
  return(us)


if __name__ == "__main__":
  """
  info = {'ylabel': 'mass ratio', 'xlabel': 'log10(start mass)'}
  y, x = [], [i for i in range(1, 10)]
  for j in range(5, 10):
    y.append([])
    for i in range(1, 10):
      y[-1].append(merger_correction(10**j, i, 0)) # Mergers of galaxies of 10^7 at z=0, various u

  graph.line(y, x=x, info=info)
  plt.show()
  """

  a = integrated_merger_corr(1e6, 1, 2)
  print("z = 1 to 2, mass = 6:", a)
  a = integrated_merger_corr(1e7, 1, 2)
  print("z = 1 to 2, mass = 7:", a)
  a = integrated_merger_corr(1e8, 1, 2)
  print("z = 1 to 2, mass = 8:", a)
  a = integrated_merger_corr(1e9, 1, 2)
  print("z = 1 to 2, mass = 9:", a)
