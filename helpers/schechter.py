#!/usr/bin/python3

import math
import sys
def schechter(m, ms, a, phi_s):
  phi_s = 10 ** phi_s
  ret = math.log(10) * phi_s * (10 ** ((m - ms) * (1 + a))) * (math.e ** (-10 ** (m - ms)))
  return(math.log10(ret))


# z is not used. Included so that the same data for the param_dub_schechter func can be used
def dub_schechter(m, ms, a1, phi_s1, a2, phi_s2, z):
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

# a = [ [x], [y], [z]]
# b = [ q, w, e]
# ret = [ [x, q], [y, w], [z, e]]
def join_two(a, b):
  try:
    assert(len(a) == len(b))
    assert(type(a) == list)
    for i in a:
      assert(type(i) == list)
  except AssertionError:
    sys.exit('Bad args to join_two')

  ret = []
  for i in range(len(a)):
    ret.append(a[i])
    ret[-1].append(b[i])
  return ret
