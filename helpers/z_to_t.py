#!/usr/bin/env python

"""
Modified from code found here:
http://www.astro.ucla.edu/~wright/CosmoCalc.html
"""
import sys
import math

def old_t_from_z(z):
  H0 = 69.6 # Hubble constant
  WM = 0.286                       # Omega(matter)
  WV = 1.0 - WM - 0.4165/(H0*H0)  # Omega(vacuum) or lambda

# initialize constants
  universe_age = 13.7203671192 #Gyr
  WR = 0.        # Omega(radiation)
  WK = 0.        # Omega curvaturve = 1-Omega(total)
  Tyr = 977.8    # coefficent for converting 1/H into Gyr
  age = 0.5      # age of Universe in units of 1/H0
  age_Gyr = 0.0  # value of age in Gyr
  zage = 0.1     # age of Universe at redshift z in units of 1/H0
  zage_Gyr = 0.0 # value of zage in Gyr
  a = 1.0        # 1/(1+z), the scale factor of the Universe
  az = 0.5       # 1/(1+z(object))

  h = H0/100.
  WR = 4.165E-5/(h*h)   # includes 3 massless neutrino species, T0 = 2.72528
  WK = 1-WM-WR-WV
  az = 1.0/(1+1.0*z)
  age = 0.
  n=1000         # number of points in integrals
  for i in range(n):
    a = az*(i+0.5)/n
    adot = math.sqrt(WK+(WM/a)+(WR/(a*a))+(WV*a*a))
    age = age + 1./adot

  zage = az*age/n
  zage_Gyr = (Tyr/H0)*zage

  return(round(universe_age - zage_Gyr, 10))

# Would be nice to do this properly...
# Tells you the Z value of something t years ago
# t must be in Gyrs
def old_z_from_t(t):
  iters = 50 # Check but think this is more than enough
  start = 0.
  stop = 6. # Gets you to 12.7 Gyrs ago...
  target = t
  for i in range(iters):
    # Guess is the number of years ago at the test Z (start+stop)/2
    # If guess is too big (too many years ago), we want a smaller Z
    guess = t_from_z((start+stop)/2)
    if guess > target:
      stop = (start + stop) / 2
    elif guess < target:
      start = (start + stop) / 2
    else: # Unlikely...
      return((start + stop) / 2)
  if stop == 6:
    raise Exception('Too long ago - change stop time of search')

  return((start + stop)/ 2)

c1, c2, coz, cot = 13.9, 13.1, 0.7, 6
def t_from_z(z):
  if z > 3:
    raise Exception('Z too high!')
  c = c1*(1/coz*(coz-z) if z < coz else 0) + c2*(1/coz*z if z < coz else 1)
  return(c - (2*c/(1 + (1+z)**2)))

def z_from_t(t):
  if t > 11.6:
    raise Exception('T too high!')
  c = c1*(1/cot*(cot-t) if t < cot else 0) + c2*(1/cot*t if t < cot else 1)
  return((-2 + math.sqrt(-4 + 8 * c/(c-t)))/2)
