#!/usr/bin/env python3

"""
Reads the star formation rate of local group dwarfs and formats it in the way we want it!
"""

import sys

if __name__ == "__main__":
  f = open('sfh_data', 'r')
  for line in f:
    if line == '###\n':
      break

  legend = ['name', 'total'] + ["m" + str(i/10) for i in range(101, 65, -1)]
  res = []
  unc = []
  unc_totals = []
  names = []
  totals = []
  res_locations = [6 + 5*i for i in range(50)]
  unc_locations =  [[5*i-2, 5*i] for i in range(1,52)]
  for line in f:
    x = [i for i in line[18:].split(' ') if i != '']
    totals.append(x[1])
    res.append([float(x[i]) for i in res_locations])

    unc_totals.append([float(x[unc_locations[0][0]]), float(x[unc_locations[0][1]])])
    unc.append([ [float(x[i[0]]), float(x[i[1]])] for i in unc_locations[1:]])

    names.append(line[:18].rstrip(' '))


  #print(unc_totals)
  for i in unc:
    print(i, ',')

  """
  for i in res:
    print(i)
  print(names)
  print(totals)
  print(legend)
  """
