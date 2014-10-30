#!/usr/bin/python3

import math
def schechter(m, ms, a, phi_s):
  phi_s = 10 ** phi_s
  ret = math.log(10) * phi_s * (10 ** ((m - ms) * (1 + a))) * (math.e ** (-10 ** (m - ms)))
  return(math.log10(ret))


def dub_schechter(m, ms, a1, phi_s1, a2, phi_s2):
  phi_s1 = 10 ** phi_s1
  phi_s2 = 10 ** phi_s2

  a = math.log(10) * math.e ** (-10 ** (m - ms)) * 10 ** (m - ms)
  b = phi_s1 * 10 ** ((m - ms) * a1) + phi_s2 * 10 ** ((m - ms) * a2)
  return(math.log10(a * b))
