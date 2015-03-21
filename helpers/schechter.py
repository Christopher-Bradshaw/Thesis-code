#!/usr/bin/env python3

import math
import sys
import helpers.graph
import helpers.helpers as h
import helpers.z_to_t as z_to_t
import matplotlib.pyplot as plt

# Input is exactly the same as data.schechter.single (except for no z) and required m
def schechter(m, ms, a, phi_s):
  phi_s = 10 ** phi_s
  ret = math.log(10) * phi_s * (10 ** ((m - ms) * (1 + a))) * (math.e ** (-10 ** (m - ms)))
  return(math.log10(ret))

# Input is exactly the same as data.schechter.double (except for no z) and required m
def double_schechter(m, ms, a1, phi_s1, a2, phi_s2):
  phi_s1 = 10 ** phi_s1
  phi_s2 = 10 ** phi_s2

  a = math.log(10) * math.e ** (-10 ** (m - ms)) * 10 ** (m - ms)
  b = phi_s1 * 10 ** ((m - ms) * a1) + phi_s2 * 10 ** ((m - ms) * a2)
  return(math.log10(a * b))

def param_double_schechter(m, z):
  a1 = -0.39
  a2 = -1.53
  phi_s1 = -2.46 + 0.07*z - 0.28*z*z
  phi_s2 = -3.11 - 0.18*z - 0.03*z*z
  ms = 10.72 - 0.13*z + 0.11*z*z
  return(double_schechter(m, ms, a1, phi_s1, a2, phi_s2))

# Given a min value, a max value, a target finds the value closest to the target after some number of iterations
# Target is a number density
# Returns the mass at that number density
def binary_search(target, z, start=0, stop=0, iters=0):
  # Don't mess with these unless you have good reason
  start = start if start else 2
  stop = stop if stop else 12
  iters = iters if iters else 100

  for i in range(iters):
    guess = param_dub_schechter((start+stop)/2, z)
    # guess = dub_schechter((start+stop)/2, *z_params[:-1]) # when passing all params
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
  target = param_dub_schechter(m, z0)
  m1 = binary_search(target, z1)
  return(m1)
