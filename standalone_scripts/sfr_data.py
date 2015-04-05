#!/usr/bin/env python3

"""
Reads the star formation data from http://iopscience.iop.org/0004-637X/795/2/104/pdf/apj_795_2_104.pdf
"""
import sys
f = open('sfr_data', 'r')

z1 = [0.5, 1, 1.5, 2]
z2 = [i+0.5 for i in z1]
zi = -1
out = []
for line in f:
  if 'z' in line:
    zi += 1
    continue

  a = line.rstrip().split('\t\t') + [z1[zi], z2[zi]]
  b = []
  for i in a:
    try:
      b.append(float(i))
    except:
      b.append(None)
  out.append(b)

for i in out:
  print(i)
